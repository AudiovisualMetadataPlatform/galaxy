import collections
import os

import pytest

from galaxy.datatypes.registry import Registry
<<<<<<< HEAD
=======
from galaxy.util.checkers import (
    is_bz2,
    is_gzip,
    is_zip
)
>>>>>>> refs/heads/release_21.01
from galaxy.util.hash_util import md5_hash_file
<<<<<<< HEAD
from .test_upload_configuration_options import BaseUploadContentConfigurationTestCase
=======
from galaxy_test.driver import integration_util
from .test_upload_configuration_options import BaseUploadContentConfigurationInstance
>>>>>>> refs/heads/release_21.01

SCRIPT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
TEST_FILE_DIR = '%s/../../lib/galaxy/datatypes/test' % SCRIPT_DIRECTORY
TEST_DATA = collections.namedtuple('UploadDatatypesData', 'path datatype uploadable')
GALAXY_ROOT = os.path.abspath('%s/../../' % SCRIPT_DIRECTORY)
DATATYPES_CONFIG = os.path.join(GALAXY_ROOT, 'lib/galaxy/config/sample/datatypes_conf.xml.sample')
PARENT_SNIFFER_MAP = {'fastqsolexa': 'fastq'}


def find_datatype(registry, filename):
    # match longest extension first
    sorted_extensions = sorted(registry.datatypes_by_extension.keys(), key=len, reverse=True)
    for extension in sorted_extensions:
        if filename.endswith(extension) or filename.startswith(extension):
            return registry.datatypes_by_extension[extension]
    raise Exception("Couldn't guess datatype for file '%s'" % filename)


def collect_test_data():
    registry = Registry()
    registry.load_datatypes(root_dir=GALAXY_ROOT, config=DATATYPES_CONFIG)
    test_files = os.listdir(TEST_FILE_DIR)
    files = [os.path.join(TEST_FILE_DIR, f) for f in test_files]
    datatypes = [find_datatype(registry, f) for f in test_files]
    uploadable = [datatype.file_ext in registry.upload_file_formats for datatype in datatypes]
    test_data_description = [TEST_DATA(*items) for items in zip(files, datatypes, uploadable)]
    return {os.path.basename(data.path): data for data in test_data_description}


class UploadTestDatatypeDataTestCase(BaseUploadContentConfigurationTestCase):
    framework_tool_and_types = False
    datatypes_conf_override = DATATYPES_CONFIG
    object_store_config = None
    object_store_config_path = None

    def runTest(self):
        # we don't want to run the standard unittest tests when we setup UploadTestDatatypeDataTestCase
        pass


@pytest.fixture(scope='module')
def instance():
    instance = UploadTestDatatypeDataTestCase()
    instance.setUpClass()
    instance.setUp()
    yield instance
    instance.tearDownClass()


<<<<<<< HEAD
@pytest.fixture
def temp_file():
    with tempfile.NamedTemporaryFile(delete=True, mode='wb') as fh:
        yield fh


TEST_CASES = collect_test_data()
=======
registry = Registry()
registry.load_datatypes(root_dir=GALAXY_ROOT, config=DATATYPES_CONFIG)
TEST_CASES = collect_test_data(registry)
>>>>>>> refs/heads/release_21.01


@pytest.mark.parametrize('test_data', TEST_CASES.values(), ids=list(TEST_CASES.keys()))
def test_upload_datatype_auto(instance, test_data, temp_file):
<<<<<<< HEAD
=======
    upload_datatype_helper(instance, test_data, temp_file)


def upload_datatype_helper(instance, test_data, temp_file):
    is_compressed = False
    for is_method in (is_bz2, is_gzip, is_zip):
        is_compressed = is_method(test_data.path)
        if is_compressed:
            break
>>>>>>> refs/heads/release_21.01
    with open(test_data.path, 'rb') as content:
        if hasattr(test_data.datatype, 'sniff') or 'false' in test_data.path:
            file_type = 'auto'
        else:
            file_type = test_data.datatype.file_ext
        dataset = instance.dataset_populator.new_dataset(instance.history_id, content=content, wait=False, file_type=file_type)
    dataset = instance.dataset_populator.get_history_dataset_details(instance.history_id, dataset=dataset, assert_ok=False)
    expected_file_ext = test_data.datatype.file_ext
    # State might be error if the datatype can't be uploaded
    if dataset['state'] == 'error' and not test_data.uploadable:
        # Some things can't be uploaded, if attempting to upload these datasets we mention why
        assert 'invalid' in dataset['misc_info'] or 'unsupported' in dataset['misc_info']
        return
    elif dataset['state'] == 'error' and 'empty' in dataset['misc_info']:
        return
    else:
        # state should be OK
        assert dataset['state'] == 'ok'
    # Check that correct datatype has been detected
    if 'false' in test_data.path:
        # datasets with false in their name are not of a specific datatype
        assert dataset['file_ext'] != PARENT_SNIFFER_MAP.get(expected_file_ext, expected_file_ext)
    else:
        assert dataset['file_ext'] == PARENT_SNIFFER_MAP.get(expected_file_ext, expected_file_ext)
    # download file and verify it hasn't been manipulated
    temp_file.write(instance.dataset_populator.get_history_dataset_content(history_id=instance.history_id,
                                                                           dataset=dataset,
                                                                           type='bytes',
                                                                           assert_ok=False,
                                                                           raw=True))
    temp_file.flush()
    assert md5_hash_file(test_data.path) == md5_hash_file(temp_file.name)
