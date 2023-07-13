#!/bin/env amp_python.sif

import requests
import logging
import argparse
import base64
from time import time
from pathlib import Path
import hashlib
import json

# Ying mentioned this API for getting all data:
# /api/invocations?key=<redacted>f&view=element&step_details=true&user_id=<redacted>
# but she's not actually using that one.  


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", default=False, action="store_true", help="Turn on debugging")
    parser.add_argument("conf", help="Configuration file (url\\nusername\\npassword)")
    parser.add_argument("outdir", help="Output directory for retrieved data")

    args = parser.parse_args()
    logging.basicConfig(format="%(asctime)s [%(levelname)-8s] (%(filename)s:%(lineno)d)  %(message)s", 
                        level=logging.DEBUG if args.debug else logging.INFO)

    # get the configuration
    try:
        with open(args.conf) as f:
            galaxy_url = f.readline().strip().rstrip('/')
            galaxy_user = f.readline().strip()
            galaxy_password = f.readline().strip()
    except Exception as e:
        logging.error(f"Cannot read config file: {e}")
        exit(1)

    # make sure out output dir is a thing
    args.outdir = Path(args.outdir)
    if not args.outdir.is_dir():
        logging.error("Output directory specified is not actually a directory")
        exit(1)
    
    # request our API key    
    authorization = base64.b64encode(f"{galaxy_user}:{galaxy_password}".encode())
    r = requests.get(f"{galaxy_url}/api/authenticate/baseauth",
                     headers={'Authorization': authorization})
    if r.status_code != 200:
        logging.error(f"Cannot login to galaxy to get API key: {r.content}")
        exit(1)
    galaxy_api_key = r.json()['api_key']

    # recreate the code that runs at 1am
    if True:
        logging.info("Get all of the workflows")
        start = time()
        r = requests.get(f"{galaxy_url}/api/workflows",
                        headers={'x-api-key': galaxy_api_key})
        workflows = r.json()
        logging.info(f"Got {len(workflows)} workflows in {time() - start} seconds")
        
        for workflow in workflows:
            start = time()
            logging.info(f"Getting workflow invocations for {workflow['id']}")
            r = requests.get(f"{galaxy_url}/api/invocations",
                            # somehow our code is calling with a history_id field.  
                            # It looks like it comes from the "findByItemCollectionActiveTrueAndHistoryIdNotNull"
                            # method.  Which doesn't have an implementation in the repo.
                            params={'workflow_id': workflow['id'],
                                    'view': 'element',
                                    'step_details': 'true',  # substantially faster when false
                                    },
                            headers={'x-api-key': galaxy_api_key})
            invocations = r.json()
            s = 0
            for i in invocations:
                s += len(i['steps'])
            logging.info(f"Got {len(invocations)} invocations for workflow {workflow['id']} with {s} steps (total) in {time() - start} seconds")
            if workflow['id'] == '2682819e19c65e80':
                print(invocations)
    else:
        md5s = {}
    
        with open(args.outdir / "calls.txt") as f:
            for url in f.readlines():
                url = url.strip()
                start = time()
                logging.info(f"Replay {url}")
                r = requests.get(f"{galaxy_url}{url}",
                                # somehow our code is calling with a history_id field.  
                                # It looks like it comes from the "findByItemCollectionActiveTrueAndHistoryIdNotNull"
                                # method.  Which doesn't have an implementation in the repo.
                )
                t = time() - start                
                res = r.content
                md5 = hashlib.md5(res).hexdigest()
                logging.info(f"Result: {md5} in {t} seconds")
                if not (args.outdir / md5).exists():
                    with open(args.outdir / md5, "wb") as f:
                        f.write(res)
                if md5 not in md5s:
                    md5s[md5] = {}
                if url not in md5s[md5]:
                    md5s[md5][url] = []
                md5s[md5][url].append(t)

        with open(args.outdir / "replay.json", "w") as f:
            json.dump(md5s, f)
        logging.info("Output in /tmp/replay.json")

    exit(0)











if __name__ == "__main__":
    main()