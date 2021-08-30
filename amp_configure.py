#!/bin/env python3
#
# Configure the galaxy instance
#

import argparse
import logging
from pathlib import Path
import sys
import os
import yaml
from amp_bootstrap_utils import read_galaxy_config, write_galaxy_config, run_cmd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', default=False, action='store_true', help="Turn on debugging")
    parser.add_argument('--force', default=False, action='store_true', help="Force a config reset")
    parser.add_argument('config', help="Configuration file")
    args = parser.parse_args()
    logging.basicConfig(format="%(asctime)s [%(levelname)-8s] (%(filename)s:%(lineno)d)  %(message)s",
                        level=logging.DEBUG if args.debug else logging.INFO)

    galaxydir = Path(sys.path[0]).resolve()
    logging.debug(f"Moving to galaxy directory {galaxydir}")
    os.chdir(galaxydir)
    
    logging.debug(f"Loading configuration file: {args.config}")
    with open(args.config) as f:
        config = yaml.safe_load(f)
    
    if Path('./config/galaxy.yml').exists() and not args.force:
        logging.info("Using existing configuration in config/galaxy.yml")
        gconfig = read_galaxy_config('./config/galaxy.yml')
    else:
        logging.info("Restoring default configuration from config/galaxy.yml.sample.amp")
        gconfig = read_galaxy_config('./config/galaxy.yml.sample.amp')

    for top in config['galaxy']:
        for key in config['galaxy'][top]:
            gconfig[top][key] = config['galaxy'][top][key]

    if gconfig['uwsgi'].get('enable-metrics', True):
        # turn on the metrics subsystem for UWSGI
        logging.debug("Enabling uwsgi metrics")
        gconfig['uwsgi'].update({
            'dlopen': 'amp_metrics/system_metrics.so',
            'metric': [
                'name=system_load,collector=func,arg1=load_average,freq=3',
                'name=system_swap,collector=func,arg1=swap,freq=3',
                'name=system_ram,collector=func,arg1=memory,freq=3',
                'name=cpu_user,collector=func,arg1=cpu_user,freq=3',
                'name=cpu_system,collector=func,arg1=cpu_system,freq=3',
                'name=cpu_iowait,collector=func,arg1=cpu_iowait,freq=3',
                'name=cpu_idle,collector=func,arg1=cpu_idle,freq=3',
            ],
            'logger': 'file:logfile=logs/uwsgi.log,maxsize=100000000',
            'req-logger': 'file:logfile=logs/requests.log,maxsize=100000000',
            'logformat': '0%(time)|%(wid)|%(core)|%(secs)|%(metric.system_load)|%(metric.system_ram)|%(metric.system_swap)|%(metric.cpu_user)|%(metric.cpu_system)|%(metric.cpu_idle)|%(metric.cpu_iowait)|%(addr)|%(var.X-FORWARDED-FOR)|%(method)|%(uri)',
        })
        # build the metrics plugin
        logging.debug("Building uwsgi metrics module")
        run_cmd(['make'], 'Cannot build system metrics module', workdir=galaxydir / 'amp_metrics')
    else:
        # clear out the metrics keys
        for n in ('dlopen', 'metric', 'logger', 'req-logger', 'logformat'):
            gconfig['uwsgi'].pop(n, None)
        # put in the default values
        gconfig['uwsgi'].update({
            'req-logger': 'file:logfile=logs/requests.log,maxsize=100000000',
            'logformat': '0%(time)|%(wid)|%(core)|%(secs)|%(addr)|%(var.X-FORWARDED-FOR)|%(method)|%(uri)',
        })        


    # validate the configuration
    required = {
        'uwsgi': ['http'],
        'galaxy': ['admin_users', 'tool_config_file', 'tool_path']
    }
    for top in required:
        for key in required[top]:
            if key not in gconfig[top]:
                logging.warning(f"The key {top}/{key} is missing from the configuration. Galaxy may not start correctly")

    write_galaxy_config(gconfig, "./config/galaxy.yml")

    
    


if __name__ == "__main__":
    main()