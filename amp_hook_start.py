#!/bin/env python3
# The start hook doesn't take any arguments (except possibly the --debug flag)
# but it is passed the AMP_ROOT and AMP_DATA_ROOT environment variables

import argparse
import os
from amp.config import load_amp_config
from amp.logging import setup_logging
import logging
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", default=False, action="store_true", help="Turn on debugging")
    args = parser.parse_args()

    setup_logging(None, args.debug)

    # There's an integrated_tool_panel.xml that will sometimes
    # remember previous configuration settings for the tool
    # panel.  Remove the file and let galaxy rebuild it.
    itp = Path(os.environ['AMP_ROOT'], 'galaxy', 'config', 'integrated_tool_panel.xml')
    if itp.exists():
        itp.unlink()

    try:
        subprocess.run([f"{os.environ['AMP_ROOT']}/galaxy/run.sh", "start"], check=True)
    except Exception as e:
        logging.error(f"Cannot start galaxy: {e}")


if __name__ == "__main__":
    main()

