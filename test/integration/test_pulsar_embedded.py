"""Integration tests for the Pulsar embedded runner."""

import os

from galaxy_test.driver import integration_util

SCRIPT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
EMBEDDED_PULSAR_JOB_CONFIG_FILE = os.path.join(SCRIPT_DIRECTORY, "embedded_pulsar_job_conf.xml")


class EmbeddedPulsarIntegrationTestCase(integration_util.IntegrationTestCase):
    """Start a Pulsar job."""

    framework_tool_and_types = True

    @classmethod
    def handle_galaxy_config_kwds(cls, config):
        config["job_config_file"] = EMBEDDED_PULSAR_JOB_CONFIG_FILE

    def test_tool_simple_constructs(self):
        self._run_tool_test("simple_constructs")

    def test_multi_data_param(self):
        self._run_tool_test("multi_data_param")

<<<<<<< HEAD
    def test_work_dir_outputs(self):
        self._run_tool_test("output_filter")
=======
test_tools = integration_util.integration_tool_runner([
    "simple_constructs",
    "multi_data_param",
    "output_filter",
    "vcf_bgzip_test",
    "environment_variables",
])
>>>>>>> refs/heads/release_21.01
