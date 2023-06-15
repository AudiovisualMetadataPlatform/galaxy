#!/bin/env python3
# This script will be run when the AMP system is reconfigured.  It will
# write the configuration files that galaxy needs, driven by the amp
# configuration file.
#
# No arguments, but the AMP_ROOT and AMP_DATA_ROOT environment variables
# will be set by the caller so it can find all things AMP.

import argparse
import logging
from pathlib import Path
import os
import yaml
import subprocess
import random
from amp.config import load_amp_config
from amp.logging import setup_logging

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', default=False, action='store_true', help="Turn on debugging")    
    args = parser.parse_args()

    # set up the standard logging
    setup_logging(None, args.debug)

    # grab the configuration file
    config = load_amp_config()

    # set amp_root
    amp_root = Path(os.environ['AMP_ROOT'])


    # config/galaxy.yml isn't a real YAML file, so writing this is actually a manual dump
    # for the uwsgi section, and a real yaml dump for the galaxy section.
    with open(amp_root / "galaxy/config/galaxy.yml", "w") as f:
        f.write("## Automatically generated file, do no edit\n")
        f.write("uwsgi:\n")
        # the host/port for galaxy
        port = config['amp']['port'] + 2
        galaxy_port = port  # we'll need this value later.
        host = config['galaxy'].get('host', '')
        f.write(f"  http: {host}:{port}\n")
        
        # the application mount settings        
        f.write(f"  mount: {config['galaxy']['root']}=galaxy.webapps.galaxy.buildapp:uwsgi_app()\n")
        f.write(f"  manage-script-name: true\n")

        # do the uwsgi things
        for k,v in config['galaxy']['uwsgi'].items():
            if isinstance(v, bool):
                f.write(f"  {k}: {'true' if v else 'false'}\n")                
            elif isinstance(v, list):
                for x in v:
                    f.write(f"  {k}: {x}\n")
            else:
                f.write(f"  {k}: {v}\n")

        # Now for the actual galaxy config stuff.  It is really
        # yaml, so we can just build the data structure in memory
        # and append it to the file.
        galaxy = config['galaxy']['galaxy']

        # the admin user
        galaxy['admin_users']  = config['galaxy']['admin_username']
        
        # id_secret -- set it if we haven't yet.
        if config['galaxy']['id_secret'] == 'CHANGE ME':
            # create a new random id_secret and save it to the runtime
            # config area
            logging.info("Generating a new id_secret")
            id_secret = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=16))
            rdata = {'galaxy': {'id_secret': id_secret}}
            with open(amp_root / "data/package_config/galaxy_idsecret.yaml", "w") as x:
                yaml.safe_dump(rdata, x)
            config = load_amp_config()
        
        galaxy['id_secret'] = config['galaxy']['id_secret']
        f.write(yaml.safe_dump({'galaxy': galaxy}))
        f.write("\n")

    # set up job_conf.xml for LWLW jobs
    with open(amp_root / "galaxy/config/job_conf.xml", "w") as f:
        f.write("""<?xml version="1.0"?>
<job_conf>
    <plugins workers="4">
        <!-- "workers" is the number of threads for the runner's work queue.
             The default from <plugins> is used if not defined for a <plugin>.
          -->
        <plugin id="local" type="runner" load="galaxy.jobs.runners.local:LocalJobRunner" workers="4"/>
        <plugin id="lwlw" type="runner" load="galaxy.jobs.runners.amp_lwlw:LwlwRunner" workers="1"/>
     </plugins>
    <destinations default="local">
        <destination id="local" runner="local"/>
        <destination id="lwlw-container" runner="lwlw"/>
    </destinations>
    <tools>\n""")        
        if 'lwlw_mgms' in config['galaxy']:
            for tool in config['galaxy']['lwlw_mgms']:
                if config['galaxy']['lwlw_mgms'][tool]:
                    f.write(f'        <tool id="{tool}" destination="lwlw-container"/>\n')
        f.write("""    </tools>
</job_conf>\n""")


    # set up the galaxy python
    logging.info("Installing galaxy python and node")
    os.environ['GALAXY_ROOT'] = str(amp_root / "galaxy")
    here = os.getcwd()
    os.chdir(amp_root / "galaxy")
    try:
        subprocess.run(['scripts/common_startup.sh'], check=True)
    except Exception as e:
        logging.error(f"Could not set up galaxy python: {e}")
        exit(1)
    galaxy_python = str(amp_root / "galaxy/.venv/bin/python")

    # Now that there's a configuration (and python), let's create the DB (if needed)
    # and create the user.  
    logging.info("Creating galaxy database")
    subprocess.run([str(amp_root / "galaxy/create_db.sh")], check=True)
    # now that there's a database, we need to have an admin user created, with the
    # password specified.  Luckily, there's a script at 
    # https://gist.github.com/jmchilton/1979583 that was referenced in scripts/db_shell.py
    # that shows how to set up an administration user.  galaxy_configure.py is based 
    # heavily on those things.
    try:
        p = subprocess.run([galaxy_python, amp_root /  "galaxy/galaxy_configure.py", 
                            config['galaxy']['admin_username'], config['galaxy']['admin_password'], config['galaxy']['id_secret']],
                        check=True, stdout=subprocess.PIPE, encoding='utf-8')
        if not p.stdout.startswith('user_id='):
            raise ValueError("Galaxy configuration didn't return a user_id")
        (_, config['galaxy']['user_id']) = p.stdout.splitlines()[0].split('=', 1)
        logging.info(f"Galaxy user ID: {config['galaxy']['user_id']}")
        # write this value to data/config/galaxy_user.yaml
        with open(amp_root / "data/package_config/galaxy_user.yaml", "w") as f:
            yaml.safe_dump({'galaxy': {'user_id': config['galaxy']['user_id']},
                            'amp': {'galaxy_port': galaxy_port}}, f)

    except Exception as e:
        logging.error(f"Galaxy database config failed: {e}")
        exit(1)

    logging.info("Creating the galaxy toolbox configuration")
    with open(amp_root / "galaxy/config/tool_conf.xml", "w") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<toolbox monitor="true">\n')
        counter = 0
        for s in config['galaxy']['toolbox']:
            f.write(f'  <section id="sect_{counter}" name="{s}">\n')
            for t in config['galaxy']['toolbox'][s]:
                f.write(f'    <tool file="{t}"/>\n')
            f.write("  </section>\n")
            counter += 1
        f.write("</toolbox>\n")


if __name__ == "__main__":
    main()