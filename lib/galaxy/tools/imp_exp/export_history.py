#!/usr/bin/env python
"""
Export a history to an archive file using attribute files.

usage: %prog history_attrs dataset_attrs job_attrs out_file
    -G, --gzip: gzip archive file
"""

import json
import optparse
import os
import sys
import tarfile
from json import dumps, loads

<<<<<<< HEAD
from galaxy.util import FILENAME_VALID_CHARS
=======
from galaxy.model.store import tar_export_directory
from galaxy.util import unicodify
>>>>>>> refs/heads/release_21.01


def get_dataset_filename(name, ext, hid):
    """
    Builds a filename for a dataset using its name an extension.
    """
    base = ''.join(c in FILENAME_VALID_CHARS and c or '_' for c in name)
    return base + "_%s.%s" % (hid, ext)


def create_archive(history_attrs_file, datasets_attrs_file, jobs_attrs_file, out_file, gzip=False):
    """Create archive from the given attribute/metadata files and save it to out_file."""
    tarfile_mode = "w"
    if gzip:
        tarfile_mode += ":gz"
    try:

        history_archive = tarfile.open(out_file, tarfile_mode)

        # Read datasets attributes from file.
        with open(datasets_attrs_file) as datasets_attr_in:
            datasets_attr_str = ''
            buffsize = 1048576
            try:
                while True:
                    datasets_attr_str += datasets_attr_in.read(buffsize)
                    if not datasets_attr_str or len(datasets_attr_str) % buffsize != 0:
                        break
            except OverflowError:
                pass
        datasets_attrs = loads(datasets_attr_str)

        # Add datasets to archive and update dataset attributes.
        # TODO: security check to ensure that files added are in Galaxy dataset directory?
        for dataset_attrs in datasets_attrs:
            if dataset_attrs['exported']:
                dataset_file_name = dataset_attrs['file_name']  # Full file name.
                dataset_hid = dataset_attrs['hid']
                dataset_archive_name = os.path.join('datasets',
                                                    get_dataset_filename(dataset_attrs['name'], dataset_attrs['extension'], dataset_hid))
                history_archive.add(dataset_file_name, arcname=dataset_archive_name)

                # Include additional files for example, files/images included in HTML output.
                extra_files_path = dataset_attrs['extra_files_path']
                if extra_files_path:
                    try:
                        file_list = os.listdir(extra_files_path)
                    except OSError:
                        file_list = []

                    if len(file_list):
                        dataset_extra_files_path = 'datasets/extra_files_path_%s' % dataset_hid
                        for fname in file_list:
                            history_archive.add(os.path.join(extra_files_path, fname),
                                                arcname=(os.path.join(dataset_extra_files_path, fname)))
                        dataset_attrs['extra_files_path'] = dataset_extra_files_path
                    else:
                        dataset_attrs['extra_files_path'] = ''

                # Update dataset filename to be archive name.
                dataset_attrs['file_name'] = dataset_archive_name

        # Rewrite dataset attributes file.
        with open(datasets_attrs_file, 'w') as datasets_attrs_out:
            datasets_attrs_out.write(dumps(datasets_attrs))

        # Finish archive.
        history_archive.add(history_attrs_file, arcname="history_attrs.txt")
        history_archive.add(datasets_attrs_file, arcname="datasets_attrs.txt")
        if os.path.exists(datasets_attrs_file + ".provenance"):
            history_archive.add(datasets_attrs_file + ".provenance", arcname="datasets_attrs.txt.provenance")
        history_archive.add(jobs_attrs_file, arcname="jobs_attrs.txt")
        history_archive.close()

        # Status.
        return 'Created history archive.'
    except Exception as e:
<<<<<<< HEAD
        return 'Error creating history archive: %s' % str(e), sys.stderr
=======
        print('Error creating history archive: %s' % unicodify(e), file=sys.stderr)
        return 1
    finally:
        shutil.rmtree(export_directory, ignore_errors=True)
>>>>>>> refs/heads/release_21.01


def main():
    # Parse command line.
    parser = optparse.OptionParser()
    parser.add_option('-G', '--gzip', dest='gzip', action="store_true", help='Compress archive using gzip.')
<<<<<<< HEAD
    (options, args) = parser.parse_args()
=======
    parser.add_option('--galaxy-version', dest='galaxy_version', help='Galaxy version that initiated the command.', default=None)
    parser.add_option('--file-sources', type=str, help='file sources json')
    (options, args) = parser.parse_args(argv)
    galaxy_version = options.galaxy_version
    if galaxy_version is None:
        galaxy_version = "19.05"

>>>>>>> refs/heads/release_21.01
    gzip = bool(options.gzip)
<<<<<<< HEAD
    history_attrs, dataset_attrs, job_attrs, out_file = args

=======
    assert len(args) >= 2
    temp_directory = args[0]
    out_arg = args[1]

    destination_uri = None
    if "://" in out_arg:
        # writing to a file source instead of a dataset path.
        destination_uri = out_arg
        out_file = "./temp_out_archive"
    else:
        out_file = out_arg
>>>>>>> refs/heads/release_21.01
    # Create archive.
<<<<<<< HEAD
    status = create_archive(history_attrs, dataset_attrs, job_attrs, out_file, gzip)
    print(status)
=======
    exit = create_archive(temp_directory, out_file, gzip=gzip)
    if destination_uri is not None and exit == 0:
        _write_to_destination(options.file_sources, os.path.abspath(out_file), destination_uri)
    return exit


def _write_to_destination(file_sources_path, out_file, destination_uri):
    file_sources = get_file_sources(file_sources_path)
    file_source_path = file_sources.get_file_source_path(destination_uri)
    file_source = file_source_path.file_source
    assert os.path.exists(out_file)
    file_source.write_from(file_source_path.path, out_file)


def get_file_sources(file_sources_path):
    assert os.path.exists(file_sources_path), "file sources path [%s] does not exist" % file_sources_path
    from galaxy.files import ConfiguredFileSources
    with open(file_sources_path) as f:
        file_sources_as_dict = json.load(f)
    file_sources = ConfiguredFileSources.from_dict(file_sources_as_dict)
    return file_sources
>>>>>>> refs/heads/release_21.01


if __name__ == "__main__":
    main()
