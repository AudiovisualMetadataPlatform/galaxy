#!/bin/env python3
#
# Install the galaxy instance
#

import argparse
import logging

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', default=False, action='store_true', help="Turn on debugging")
    parser.add_argument('--version', type=str, help="Package Version", default=None)  
    parser.add_argument('config', help="Configuration file")
    args = parser.parse_args()
    logging.basicConfig(format="%(asctime)s [%(levelname)-8s] (%(filename)s:%(lineno)d)  %(message)s",
                        level=logging.DEBUG if args.debug else logging.INFO)

    logging.info("No installation actions required")


if __name__ == "__main__":
    main()