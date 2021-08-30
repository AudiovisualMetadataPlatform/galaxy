#!/bin/env python3
#
# Control the galaxy instance
#

import argparse
import logging
from pathlib import Path
import subprocess
import sys
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', default=False, action='store_true', help="Turn on debugging")
    parser.add_argument('--version', type=str, help="Package Version", default=None)  
    parser.add_argument('action', choices=['start', 'stop', 'restart'], help="Control action")
    parser.add_argument('config', default=None, help="AMP configuration file")
    args = parser.parse_args()
    logging.basicConfig(format="%(asctime)s [%(levelname)-8s] (%(filename)s:%(lineno)d)  %(message)s",
                        level=logging.DEBUG if args.debug else logging.INFO)

    galaxydir = Path(sys.path[0]).resolve()
    logging.debug(f"Moving to galaxy directory {galaxydir}")
    os.chdir(galaxydir)
    subprocess.run(["./run.sh", args.action])


if __name__ == "__main__":
    main()