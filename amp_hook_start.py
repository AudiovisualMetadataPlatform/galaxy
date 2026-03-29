#!/bin/env python3
# The start hook doesn't take any arguments (except possibly the --debug flag)
# but it is passed the AMP_ROOT and AMP_DATA_ROOT environment variables

import argparse
import os
import socket
import time
from amp.config import load_amp_config
from amp.logging import setup_logging
import logging
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", default=False, action="store_true", help="Turn on debugging")
    args = parser.parse_args()

    # set up the standard logging
    setup_logging(None, args.debug)

    # grab the configuration file, host and port
    config = load_amp_config()
    host = config['galaxy'].get('host', '')
    port = config['amp']['port'] + 2
        
    # There's an integrated_tool_panel.xml that will sometimes
    # remember previous configuration settings for the tool
    # panel.  Remove the file and let galaxy rebuild it.
    itp = Path(os.environ['AMP_ROOT'], 'galaxy', 'config', 'integrated_tool_panel.xml')
    if itp.exists():
        itp.unlink()

    try:
        subprocess.run([f"{os.environ['AMP_ROOT']}/galaxy/run.sh", "start"], check=True)
        # Block until Galaxy is actually ready
        if not wait_for_port(port, host):
            logging.error("FATAL: Galaxy failed to respond within 10 minutes after starting.")
            exit(1)
    except Exception as e:
        logging.error(f"Cannot start galaxy: {e}")

def wait_for_port(port, host, timeout=600):
    """Blocks until the specified port is accepting connections."""
    logging.info(f"Galaxy processes signaled to start. Waiting for API on {host}:{port}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            target_host = host if host and host != '0.0.0.0' else '127.0.0.1'
            if s.connect_ex((target_host, port)) == 0:
                logging.info(f"SUCCESS: Galaxy is listening on port {port}!")
                # Optional: extra 3-sec buffer for internal app init
                time.sleep(3)
                return True
        time.sleep(10)
        logging.debug(f"Still waiting for Galaxy... ({int(time.time() - start_time)}s elapsed)")
    return False

if __name__ == "__main__":
    main()

