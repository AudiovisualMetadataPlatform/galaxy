#!/bin/env python3
#
# Build the amp-galaxy tarball for distribution
#

import argparse
import logging
import tempfile
from pathlib import Path
import sys
from amp_bootstrap_utils import run_cmd, build_package

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', default=False, action='store_true', help="Turn on debugging")
    parser.add_argument('--version', type=str, help="Package Version", default=None)  
    parser.add_argument('destdir', help="Destination directory")
    args = parser.parse_args()
    logging.basicConfig(format="%(asctime)s [%(levelname)-8s] (%(filename)s:%(lineno)d)  %(message)s",
                        level=logging.DEBUG if args.debug else logging.INFO)
    
    args.destdir = str(Path(args.destdir).resolve())
    with tempfile.TemporaryDirectory(prefix='amp_galaxy_build-') as tmpdir:
        ptmpdir = Path(tmpdir)
        logging.debug(f"Temporary directory is: {tmpdir}")
        logging.info("Copying files temp dir")
        run_cmd(['cp', '-a', '.', tmpdir], "Copy to tempdir failed", workdir=sys.path[0])
        logging.info(f"Starting distribution cleanup")
        # delete entire trees that we don't want to distribute
        to_delete = [
            # dotfiles
            '.ci', '.circleci', '.git', '.github', '.venv',
            '.dockerignore', '.gitattributes', '.gitignore', '.k8s_ci.Dockerfile',
            # configs
            'config/galaxy.yml', 'config/tool_conf.xml',
            # active data
            'logs', 'database',
            # metrics
            'amp_metrics/system_metrics', 'amp_metrics/system_metrics.so',
        ]
        to_delete = [Path(tmpdir, x) for x in to_delete]
        # Find runtime files..
        for d in ['node_modules', '__pycache__']:
            to_delete.extend(ptmpdir.glob(f"**/{d}/"))
        for d in to_delete:
            if d.exists():
                logging.debug(f"Removing {d}")
                run_cmd(['rm', '-rf', str(d)], "Failed to remove tree")
        # put back the logs and database directories
        for d in ['logs', 'database']:
            (ptmpdir / d).mkdir(parents=True, exist_ok=True)

        # create the package
        logging.info(f"Creating package in {args.destdir}")
        outfile = build_package(tmpdir, args.destdir, 'galaxy', version=args.version)
        print(outfile)


if __name__ == "__main__":
    main()
