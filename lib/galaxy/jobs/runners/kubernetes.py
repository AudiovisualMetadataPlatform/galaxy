"""
Offload jobs to a Kubernetes cluster.
"""

import logging
import re
<<<<<<< HEAD
from os import environ as os_environ
from time import sleep
=======

import yaml
>>>>>>> refs/heads/release_21.01


from six import text_type

from galaxy import model
from galaxy.jobs.runners import (
    AsynchronousJobRunner,
    AsynchronousJobState,
    JobState
)
<<<<<<< HEAD
=======
from galaxy.jobs.runners.util.pykube_util import (
    DEFAULT_JOB_API_VERSION,
    ensure_pykube,
    find_job_object_by_name,
    find_pod_object_by_name,
    galaxy_instance_id,
    Job,
    job_object_dict,
    Pod,
    produce_k8s_job_prefix,
    pull_policy,
    pykube_client_from_dict,
    stop_job,
)
from galaxy.util.bytesize import ByteSize
>>>>>>> refs/heads/release_21.01

log = logging.getLogger(__name__)

__all__ = ('KubernetesJobRunner', )


class KubernetesJobRunner(AsynchronousJobRunner):
    """
    Job runner backed by a finite pool of worker threads. FIFO scheduling
    """
    runner_name = "KubernetesRunner"

    LABEL_START = re.compile("^[A-Za-z0-9]")
    LABEL_END = re.compile("[A-Za-z0-9]$")
    LABEL_REGEX = re.compile("[^-A-Za-z0-9_.]")

    def __init__(self, app, nworkers, **kwargs):
        # Check if pykube was importable, fail if not
        ensure_pykube()
        runner_param_specs = dict(
<<<<<<< HEAD
            k8s_config_path=dict(map=str, default=os_environ.get('KUBECONFIG', None)),
=======
            k8s_config_path=dict(map=str, default=None),
>>>>>>> refs/heads/release_21.01
            k8s_use_service_account=dict(map=bool, default=False),
            k8s_persistent_volume_claim_name=dict(map=str),
            k8s_persistent_volume_claim_mount_path=dict(map=str),
            k8s_namespace=dict(map=str, default="default"),
            k8s_pod_priority_class=dict(map=str, default=None),
            k8s_affinity=dict(map=str, default=None),
            k8s_node_selector=dict(map=str, default=None),
            k8s_tolerations=dict(map=str, default=None),
            k8s_galaxy_instance_id=dict(map=str),
            k8s_timeout_seconds_job_deletion=dict(map=int, valid=lambda x: int > 0, default=30),
            k8s_job_api_version=dict(map=str, default=DEFAULT_JOB_API_VERSION),
            k8s_job_ttl_secs_after_finished=dict(map=int, valid=lambda x: x is None or int(x) >= 0, default=None),
            k8s_job_metadata=dict(map=str, default=None),
            k8s_supplemental_group_id=dict(map=str),
            k8s_pull_policy=dict(map=str, default="Default"),
            k8s_run_as_user_id=dict(map=str, valid=lambda s: s == "$uid" or s.isdigit()),
            k8s_run_as_group_id=dict(map=str, valid=lambda s: s == "$gid" or s.isdigit()),
            k8s_fs_group_id=dict(map=int),
<<<<<<< HEAD
            k8s_default_requests_cpu=dict(map=str, default=None),
            k8s_default_requests_memory=dict(map=str, default=None),
            k8s_default_limits_cpu=dict(map=str, default=None),
            k8s_default_limits_memory=dict(map=str, default=None),
            k8s_pod_retrials=dict(map=int, valid=lambda x: int > 0, default=3))
=======
            k8s_cleanup_job=dict(map=str, valid=lambda s: s in {"onsuccess", "always", "never"}, default="always"),
            k8s_pod_retries=dict(map=int, valid=lambda x: int(x) >= 0, default=3),
            k8s_walltime_limit=dict(map=int, valid=lambda x: int(x) >= 0, default=172800))
>>>>>>> refs/heads/release_21.01

        if 'runner_param_specs' not in kwargs:
            kwargs['runner_param_specs'] = dict()
        kwargs['runner_param_specs'].update(runner_param_specs)

        """Start the job runner parent object """
        super().__init__(app, nworkers, **kwargs)

<<<<<<< HEAD
        # self.cli_interface = CliInterface()

        if "k8s_use_service_account" in self.runner_params and self.runner_params["k8s_use_service_account"]:
            self._pykube_api = HTTPClient(KubeConfig.from_service_account())
        else:
            self._pykube_api = HTTPClient(KubeConfig.from_file(self.runner_params["k8s_config_path"]))
        self._galaxy_vol_name = "pvc-galaxy"  # TODO this needs to be read from params!!

=======
        self._pykube_api = pykube_client_from_dict(self.runner_params)
>>>>>>> refs/heads/release_21.01
        self._galaxy_instance_id = self.__get_galaxy_instance_id()

        self._run_as_user_id = self.__get_run_as_user_id()
        self._run_as_group_id = self.__get_run_as_group_id()
        self._supplemental_group = self.__get_supplemental_group()
        self._fs_group = self.__get_fs_group()
        self._default_pull_policy = self.__get_pull_policy()

        self._init_monitor_thread()
        self._init_worker_threads()
<<<<<<< HEAD
=======
        self.setup_volumes()

    def setup_volumes(self):
        if self.runner_params.get('k8s_persistent_volume_claims'):
            volume_claims = dict(volume.split(":") for volume in self.runner_params['k8s_persistent_volume_claims'].split(','))
        else:
            volume_claims = {}
        mountable_volumes = [{'name': claim_name, 'persistentVolumeClaim': {'claimName': claim_name}} for claim_name in volume_claims]
        self.runner_params['k8s_mountable_volumes'] = mountable_volumes
        volume_mounts = [{'name': claim_name, 'mountPath': mount_path} for claim_name, mount_path in volume_claims.items()]
        self.runner_params['k8s_volume_mounts'] = volume_mounts
>>>>>>> refs/heads/release_21.01

    def queue_job(self, job_wrapper):
        """Create job script and submit it to Kubernetes cluster"""
        # prepare the job
        # We currently don't need to include_metadata or include_work_dir_outputs, as working directory is the same
        # were galaxy will expect results.
        log.debug("Starting queue_job for job " + job_wrapper.get_id_tag())
        if not self.prepare_job(job_wrapper, include_metadata=False, modify_command_for_container=False):
            return

        job_destination = job_wrapper.job_destination

        # Construction of the Kubernetes Job object follows: http://kubernetes.io/docs/user-guide/persistent-volumes/
<<<<<<< HEAD
        k8s_job_name = self.__produce_unique_k8s_job_name(job_wrapper.get_id_tag())
        k8s_job_obj = {
            "apiVersion": self.runner_params['k8s_job_api_version'],
            "kind": "Job",
            "metadata": {
                    # metadata.name is the name of the pod resource created, and must be unique
                    # http://kubernetes.io/docs/user-guide/configuring-containers/
                    "name": k8s_job_name,
                    "namespace": self.runner_params['k8s_namespace'],
                    "labels": {"app": k8s_job_name}
            },
            "spec": self.__get_k8s_job_spec(job_wrapper)
        }
=======
        k8s_job_prefix = self.__produce_k8s_job_prefix()
        k8s_job_obj = job_object_dict(
            self.runner_params,
            k8s_job_prefix,
            self.__get_k8s_job_spec(ajs)
        )
>>>>>>> refs/heads/release_21.01

        job = Job(self._pykube_api, k8s_job_obj)
        job.create()
        job_id = job.metadata['name']

        # define job attributes in the AsyncronousJobState for follow-up
<<<<<<< HEAD
        ajs = AsynchronousJobState(files_dir=job_wrapper.working_directory, job_wrapper=job_wrapper,
                                   job_id=k8s_job_name, job_destination=job_destination)
=======
        ajs.job_id = job_id
        # store runner information for tracking if Galaxy restarts
        job_wrapper.set_external_id(job_id)
>>>>>>> refs/heads/release_21.01
        self.monitor_queue.put(ajs)

<<<<<<< HEAD
        # external_runJob_script can be None, in which case it's not used.
        external_runjob_script = None
        return external_runjob_script
=======
    def __get_overridable_params(self, job_wrapper, param_key):
        dest_params = self.__get_destination_params(job_wrapper)
        return dest_params.get(param_key, self.runner_params[param_key])
>>>>>>> refs/heads/release_21.01

    def __get_pull_policy(self):
        return pull_policy(self.runner_params)

    def __get_run_as_user_id(self):
        if "k8s_run_as_user_id" in self.runner_params:
            run_as_user = self.runner_params["k8s_run_as_user_id"]
            if run_as_user == "$uid":
                return os.getuid()
            else:
                return int(self.runner_params["k8s_run_as_user_id"])
        return None

    def __get_run_as_group_id(self):
        if "k8s_run_as_group_id" in self.runner_params:
            run_as_group = self.runner_params["k8s_run_as_group_id"]
            if run_as_group == "$gid":
                return self.app.config.gid
            else:
                return int(self.runner_params["k8s_run_as_group_id"])
        return None

    def __get_supplemental_group(self):
        if "k8s_supplemental_group_id" in self.runner_params:
            try:
                return int(self.runner_params["k8s_supplemental_group_id"])
            except Exception:
                log.warning("Supplemental group passed for Kubernetes runner needs to be an integer, value "
                         + self.runner_params["k8s_supplemental_group_id"] + " passed is invalid")
                return None
        return None

    def __get_fs_group(self):
        if "k8s_fs_group_id" in self.runner_params:
            try:
                return int(self.runner_params["k8s_fs_group_id"])
            except Exception:
                log.warning("FS group passed for Kubernetes runner needs to be an integer, value "
                         + self.runner_params["k8s_fs_group_id"] + " passed is invalid")
                return None
        return None

    def __get_galaxy_instance_id(self):
        """Parse the ID of the Galaxy instance from runner params."""
        return galaxy_instance_id(self.runner_params)

    def __produce_k8s_job_prefix(self):
        instance_id = self._galaxy_instance_id or ''
        return produce_k8s_job_prefix(app_prefix='gxy', instance_id=instance_id)

<<<<<<< HEAD
    def __get_k8s_job_spec(self, job_wrapper):
        """Creates the k8s Job spec. For a Job spec, the only requirement is to have a .spec.template."""
        k8s_job_spec = {"template": self.__get_k8s_job_spec_template(job_wrapper)}
=======
    def __get_k8s_job_spec(self, ajs):
        """Creates the k8s Job spec. For a Job spec, the only requirement is to have a .spec.template.
        If the job hangs around unlimited it will be ended after k8s wall time limit, which sets activeDeadlineSeconds"""
        k8s_job_spec = {"template": self.__get_k8s_job_spec_template(ajs),
                        "activeDeadlineSeconds": int(self.runner_params['k8s_walltime_limit'])}
        job_ttl = self.runner_params["k8s_job_ttl_secs_after_finished"]
        if self.runner_params["k8s_cleanup_job"] != "never" and job_ttl is not None:
            k8s_job_spec["ttlSecondsAfterFinished"] = job_ttl
>>>>>>> refs/heads/release_21.01
        return k8s_job_spec

<<<<<<< HEAD
    def __get_k8s_job_spec_template(self, job_wrapper):
=======
    def __force_label_conformity(self, value):
        """
        Make sure that a label conforms to k8s requirements.
        A valid label must be an empty string or consist of alphanumeric characters, '-', '_' or '.',
        and must start and end with an alphanumeric character (e.g. 'MyValue',  or 'my_value',  or '12345',
        regex used for validation is '(([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9])?')
        """
        label_val = self.LABEL_REGEX.sub("_", value)
        if not self.LABEL_START.search(label_val):
            label_val = 'x' + label_val
        if not self.LABEL_END.search(label_val):
            label_val += 'x'
        return label_val

    def __get_k8s_job_spec_template(self, ajs):
>>>>>>> refs/heads/release_21.01
        """The k8s spec template is nothing but a Pod spec, except that it is nested and does not have an apiversion
        nor kind. In addition to required fields for a Pod, a pod template in a job must specify appropriate labels
        (see pod selector) and an appropriate restart policy."""
        k8s_spec_template = {
            "metadata": {
<<<<<<< HEAD
                "labels": {"app": self.__produce_unique_k8s_job_name(job_wrapper.get_id_tag())}
=======
                "labels": {
                    "app.kubernetes.io/name": self.__force_label_conformity(ajs.job_wrapper.tool.old_id),
                    "app.kubernetes.io/instance": self.__produce_k8s_job_prefix(),
                    "app.kubernetes.io/version": self.__force_label_conformity(str(ajs.job_wrapper.tool.version)),
                    "app.kubernetes.io/component": "tool",
                    "app.kubernetes.io/part-of": "galaxy",
                    "app.kubernetes.io/managed-by": "galaxy",
                    "app.galaxyproject.org/job_id": self.__force_label_conformity(ajs.job_wrapper.get_id_tag()),
                    "app.galaxyproject.org/handler": self.__force_label_conformity(self.app.config.server_name),
                    "app.galaxyproject.org/destination": self.__force_label_conformity(
                        str(ajs.job_wrapper.job_destination.id))
                },
                "annotations": {
                    "app.galaxyproject.org/tool_id": ajs.job_wrapper.tool.id
                }
>>>>>>> refs/heads/release_21.01
            },
            "spec": {
<<<<<<< HEAD
                "volumes": self.__get_k8s_mountable_volumes(job_wrapper),
                "restartPolicy": self.__get_k8s_restart_policy(job_wrapper),
                "containers": self.__get_k8s_containers(job_wrapper)
=======
                "volumes": self.runner_params['k8s_mountable_volumes'],
                "restartPolicy": self.__get_k8s_restart_policy(ajs.job_wrapper),
                "containers": self.__get_k8s_containers(ajs),
                "priorityClassName": self.runner_params['k8s_pod_priority_class'],
                "tolerations": yaml.safe_load(self.runner_params['k8s_tolerations'] or "[]"),
                "affinity": yaml.safe_load(self.__get_overridable_params(ajs.job_wrapper,
                                                                         'k8s_affinity') or "{}"),
                "nodeSelector": yaml.safe_load(self.__get_overridable_params(ajs.job_wrapper,
                                                                             'k8s_node_selector') or "{}")
>>>>>>> refs/heads/release_21.01
            }
        }
        # TODO include other relevant elements that people might want to use from
        # TODO http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_podspec
        k8s_spec_template["spec"]["securityContext"] = self.__get_k8s_security_context()
        extra_metadata = self.runner_params['k8s_job_metadata'] or '{}'
        if isinstance(extra_metadata, str):
            extra_metadata = yaml.safe_load(extra_metadata)
        k8s_spec_template["metadata"]["labels"].update(extra_metadata.get('labels', {}))
        k8s_spec_template["metadata"]["annotations"].update(extra_metadata.get('annotations', {}))
        return k8s_spec_template

    def __get_k8s_security_context(self):
        security_context = {}
        if self._run_as_user_id:
            security_context["runAsUser"] = self._run_as_user_id
        if self._run_as_group_id:
            security_context["runAsGroup"] = self._run_as_group_id
        if self._supplemental_group and self._supplemental_group > 0:
            security_context["supplementalGroups"] = [self._supplemental_group]
        if self._fs_group and self._fs_group > 0:
            security_context["fsGroup"] = self._fs_group
        return security_context

    def __get_k8s_restart_policy(self, job_wrapper):
        """The default Kubernetes restart policy for Jobs"""
        return "Never"

    def __get_k8s_mountable_volumes(self, job_wrapper):
        """Provides the required volumes that the containers in the pod should be able to mount. This should be using
        the new persistent volumes and persistent volumes claim objects. This requires that both a PersistentVolume and
        a PersistentVolumeClaim are created before starting galaxy (starting a k8s job).
        """
        # TODO on this initial version we only support a single volume to be mounted.
        k8s_mountable_volume = {
            "name": self._galaxy_vol_name,
            "persistentVolumeClaim": {
                "claimName": self.runner_params['k8s_persistent_volume_claim_name']
            }
        }
        return [k8s_mountable_volume]

    def __get_k8s_containers(self, job_wrapper):
        """Fills in all required for setting up the docker containers to be used, including setting a pull policy if
           this has been set.
        """
        k8s_container = {
            "name": self.__get_k8s_container_name(job_wrapper),
            "image": self._find_container(job_wrapper).container_id,
            # this form of command overrides the entrypoint and allows multi command
            # command line execution, separated by ;, which is what Galaxy does
            # to assemble the command.
            # TODO possibly shell needs to be set by job_wrapper
            "command": ["/bin/bash", "-c", job_wrapper.runner_command_line],
            "workingDir": job_wrapper.working_directory,
            "volumeMounts": [{
                "mountPath": self.runner_params['k8s_persistent_volume_claim_mount_path'],
                "name": self._galaxy_vol_name
            }]
        }

        resources = self.__get_resources(job_wrapper)
        if resources:
<<<<<<< HEAD
=======
            envs = []
            if 'requests' in resources:
                requests = resources['requests']
                if 'memory' in requests:
                    envs.append({'name': 'GALAXY_MEMORY_MB', 'value': str(ByteSize(requests['memory']).to_unit('M', as_string=False))})
                if 'cpu' in requests:
                    envs.append({'name': 'GALAXY_SLOTS', 'value': str(int(math.ceil(float(requests['cpu']))))})
            elif 'limits' in resources:
                limits = resources['limits']
                if 'memory' in limits:
                    envs.append({'name': 'GALAXY_MEMORY_MB', 'value': str(ByteSize(limits['memory']).to_unit('M', as_string=False))})
                if 'cpu' in limits:
                    envs.append({'name': 'GALAXY_SLOTS', 'value': str(int(math.ceil(float(limits['cpu']))))})
>>>>>>> refs/heads/release_21.01
            k8s_container['resources'] = resources

        if self._default_pull_policy:
            k8s_container["imagePullPolicy"] = self._default_pull_policy
        # if self.__requires_ports(job_wrapper):
        #    k8s_container['ports'] = self.__get_k8s_containers_ports(job_wrapper)

        return [k8s_container]

    # def __get_k8s_containers_ports(self, job_wrapper):

    #    for k,v self.runner_params:
    #        if k.startswith("container_port_"):

    def __get_resources(self, job_wrapper):
        mem_request = self.__get_memory_request(job_wrapper)
        cpu_request = self.__get_cpu_request(job_wrapper)

        mem_limit = self.__get_memory_limit(job_wrapper)
        cpu_limit = self.__get_cpu_limit(job_wrapper)

        requests = {}
        limits = {}

        if mem_request:
            requests['memory'] = mem_request
        if cpu_request:
            requests['cpu'] = cpu_request

        if mem_limit:
            limits['memory'] = mem_limit
        if cpu_limit:
            limits['cpu'] = cpu_limit

        resources = {}
        if requests:
            resources['requests'] = requests
        if limits:
            resources['limits'] = limits

        return resources

    def __get_memory_request(self, job_wrapper):
        """Obtains memory requests for job, checking if available on the destination, otherwise using the default"""
        job_destination = job_wrapper.job_destination

        if 'requests_memory' in job_destination.params:
            return self.__transform_memory_value(job_destination.params['requests_memory'])
        return None

    def __get_memory_limit(self, job_wrapper):
        """Obtains memory limits for job, checking if available on the destination, otherwise using the default"""
        job_destination = job_wrapper.job_destination

        if 'limits_memory' in job_destination.params:
            return self.__transform_memory_value(job_destination.params['limits_memory'])
        return None

    def __get_cpu_request(self, job_wrapper):
        """Obtains cpu requests for job, checking if available on the destination, otherwise using the default"""
        job_destination = job_wrapper.job_destination

<<<<<<< HEAD
        if 'requests_cpu' in job_destinantion.params:
            return self.__transform_cpu_value(job_destinantion.params['requests_cpu'])
=======
        if 'requests_cpu' in job_destination.params:
            return job_destination.params['requests_cpu']
>>>>>>> refs/heads/release_21.01
        return None

    def __get_cpu_limit(self, job_wrapper):
        """Obtains cpu requests for job, checking if available on the destination, otherwise using the default"""
        job_destination = job_wrapper.job_destination

<<<<<<< HEAD
        if 'limits_cpu' in job_destinantion.params:
            return self.__transform_cpu_value(job_destinantion.params['limits_cpu'])
=======
        if 'limits_cpu' in job_destination.params:
            return job_destination.params['limits_cpu']
>>>>>>> refs/heads/release_21.01
        return None

    def __transform_cpu_value(self, cpu_value):
        """Transforms cpu value

           If the value is 0 and not a string, then None is returned.
           If the value is a float, then it is multiplied by 1000 and expressed as mili cpus.
           If the value is an integer, then it is and expressed as CPUs (no unit).
           If it is an already formatted string, it is returned as it was.
        """
        if not isinstance(cpu_value, str) and float(cpu_value) == 0:
            return None
        if isinstance(cpu_value, float):
            return str(int(cpu_value * 1000)) + "m"
        elif isinstance(cpu_value, int):
            return str(cpu_value)
        return cpu_value

    def __transform_memory_value(self, mem_value):
        """Transforms memory value

           If the value is 0 and not a string, then None is returned.
           If the value has a decimal part, then it is multiplied by 1000 and expressed as Megabytes.
           If the value is an integer, then it is truncated and expressed as Gigabytes.
           If it is an already formatted string, it is returned as it was.
        """
        if not isinstance(mem_value, str) and float(mem_value) == 0:
            return None
        if isinstance(mem_value, float):
            return str(int(mem_value * 1000)) + "M"
        elif isinstance(mem_value, int):
            return str(mem_value) + "G"
        return mem_value

    def __assemble_k8s_container_image_name(self, job_wrapper):
        """Assembles the container image name as repo/owner/image:tag, where repo, owner and tag are optional"""
        job_destination = job_wrapper.job_destination

        # Determine the job's Kubernetes destination (context, namespace) and options from the job destination
        # definition
        repo = ""
        owner = ""
        if 'repo' in job_destination.params:
            repo = job_destination.params['repo'] + "/"
        if 'owner' in job_destination.params:
            owner = job_destination.params['owner'] + "/"

        k8s_cont_image = repo + owner + job_destination.params['image']

        if 'tag' in job_destination.params:
            k8s_cont_image += ":" + job_destination.params['tag']

        return k8s_cont_image

    def __get_k8s_container_name(self, job_wrapper):
        # These must follow a specific regex for Kubernetes.
        raw_id = job_wrapper.job_destination.id
        if isinstance(raw_id, str):
            cleaned_id = re.sub("[^-a-z0-9]", "-", raw_id)
            if cleaned_id.startswith("-") or cleaned_id.endswith("-"):
                cleaned_id = "x%sx" % cleaned_id
            return cleaned_id
        return "job-container"

    def __get_destination_params(self, job_wrapper):
        """Obtains allowable runner param overrides from the destination"""
        job_destination = job_wrapper.job_destination
        OVERRIDABLE_PARAMS = ["k8s_node_selector", "k8s_affinity"]
        new_params = {}
        for each_param in OVERRIDABLE_PARAMS:
            if each_param in job_destination.params:
                new_params[each_param] = job_destination.params[each_param]
        return new_params

    def check_watched_item(self, job_state):
        """Checks the state of a job already submitted on k8s. Job state is an AsynchronousJobState"""
        jobs = find_job_object_by_name(self._pykube_api, job_state.job_id, self.runner_params['k8s_namespace'])

        if len(jobs.response['items']) == 1:
            job = Job(self._pykube_api, jobs.response['items'][0])
            job_destination = job_state.job_wrapper.job_destination
            succeeded = 0
            active = 0
            failed = 0

<<<<<<< HEAD
            max_pod_retrials = 1
            if 'k8s_pod_retrials' in self.runner_params:
                max_pod_retrials = int(self.runner_params['k8s_pod_retrials'])
            if 'max_pod_retrials' in job_destination.params:
                max_pod_retrials = int(job_destination.params['max_pod_retrials'])
=======
            if 'max_pod_retries' in job_destination.params:
                max_pod_retries = int(job_destination.params['max_pod_retries'])
            elif 'k8s_pod_retries' in self.runner_params:
                max_pod_retries = int(self.runner_params['k8s_pod_retries'])
            else:
                max_pod_retries = 1
>>>>>>> refs/heads/release_21.01

            # Check if job.obj['status'] is empty,
            # return job_state unchanged if this is the case
            # as probably this means that the k8s API server hasn't
            # had time to fill in the object status since the
            # job was created only too recently.
            if len(job.obj['status']) == 0:
                return job_state
            if 'succeeded' in job.obj['status']:
                succeeded = job.obj['status']['succeeded']
            if 'active' in job.obj['status']:
                active = job.obj['status']['active']
            if 'failed' in job.obj['status']:
                failed = job.obj['status']['failed']

            job_persisted_state = job_state.job_wrapper.get_state()

            # This assumes jobs dependent on a single pod, single container
<<<<<<< HEAD
            if succeeded > 0:
                self.__produce_log_file(job_state)
                with open(job_state.error_file, 'w'):
                    pass
=======
            if succeeded > 0 or job_state == model.Job.states.STOPPED:
>>>>>>> refs/heads/release_21.01
                job_state.running = False
                self.mark_as_finished(job_state)
                return None
<<<<<<< HEAD
            elif failed > 0 and self.__job_failed_due_to_low_memory(job_state):
                return self._handle_job_failure(job, job_state, reason="OOM")
            elif active > 0 and failed <= max_pod_retrials:
                job_state.running = True
=======
            elif active > 0 and failed <= max_pod_retries:
                if not job_state.running:
                    job_state.running = True
                    job_state.job_wrapper.change_state(model.Job.states.RUNNING)
>>>>>>> refs/heads/release_21.01
                return job_state
<<<<<<< HEAD
            elif failed > max_pod_retrials:
                return self._handle_job_failure(job, job_state)
            # We should not get here
            log.debug(
                "Reaching unexpected point for Kubernetes job name %s where it is not classified as succ., active nor failed.", job.name)
            log.debug("k8s full job object:\n%s", job.obj)
            return job_state
=======
            elif job_persisted_state == model.Job.states.DELETED:
                # Job has been deleted via stop_job and job has not been deleted,
                # remove from watched_jobs by returning `None`
                if job_state.job_wrapper.cleanup_job in ("always", "onsuccess"):
                    job_state.job_wrapper.cleanup()
                return None
            else:
                return self._handle_job_failure(job, job_state)
>>>>>>> refs/heads/release_21.01

        elif len(jobs.response['items']) == 0:
            if job_state.job_wrapper.get_job().state == model.Job.states.DELETED:
                # Job has been deleted via stop_job and job has been deleted,
                # cleanup and remove from watched_jobs by returning `None`
                if job_state.job_wrapper.cleanup_job in ("always", "onsuccess"):
                    job_state.job_wrapper.cleanup()
                return None
            # there is no job responding to this job_id, it is either lost or something happened.
<<<<<<< HEAD
            log.error("No Jobs are available under expected selector app=" + job_state.job_id)
            with open(job_state.error_file, 'w') as error_file:
                error_file.write("No Kubernetes Jobs are available under expected selector app=" + job_state.job_id + "\n")
=======
            log.error("No Jobs are available under expected selector app=%s", job_state.job_id)
>>>>>>> refs/heads/release_21.01
            self.mark_as_failed(job_state)
            # job is no longer viable - remove from watched jobs
            return None
        else:
            # there is more than one job associated to the expected unique job id used as selector.
<<<<<<< HEAD
            log.error("There is more than one Kubernetes Job associated to job id " + job_state.job_id)
            self.__produce_log_file(job_state)
            with open(job_state.error_file, 'w') as error_file:
                error_file.write("There is more than one Kubernetes Job associated to job id " + job_state.job_id + "\n")
=======
            log.error("More than one Kubernetes Job associated to job id '%s'", job_state.job_id)
>>>>>>> refs/heads/release_21.01
            self.mark_as_failed(job_state)
            # job is no longer viable - remove from watched jobs
            return None

<<<<<<< HEAD
    def _handle_job_failure(self, job, job_state, reason=None):
        self.__produce_log_file(job_state)
        with open(job_state.error_file, 'w') as error_file:
            if reason == "OOM":
=======
    def _handle_job_failure(self, job, job_state):
        # Figure out why job has failed
        with open(job_state.error_file, 'a') as error_file:
            if self.__job_failed_due_to_low_memory(job_state):
>>>>>>> refs/heads/release_21.01
                error_file.write("Job killed after running out of memory. Try with more memory.\n")
                job_state.fail_message = "Tool failed due to insufficient memory. Try with more memory."
                job_state.runner_state = JobState.runner_states.MEMORY_LIMIT_REACHED
            elif self.__job_failed_due_to_walltime_limit(job):
                error_file.write("DeadlineExceeded")
                job_state.fail_message = "Job was active longer than specified deadline"
                job_state.runner_state = JobState.runner_states.WALLTIME_REACHED
            else:
                error_file.write("Exceeded max number of Kubernetes pod retries allowed for job\n")
                job_state.fail_message = "More pods failed than allowed. See stdout for pods details."
        job_state.running = False
        self.mark_as_failed(job_state)
        try:
            self.__cleanup_k8s_job(job)
        except Exception:
            log.exception("Could not clean up k8s batch job. Ignoring...")
        return None

    def __cleanup_k8s_job(self, job):
        k8s_cleanup_job = self.runner_params['k8s_cleanup_job']
        stop_job(job, k8s_cleanup_job)

    def __job_failed_due_to_walltime_limit(self, job):
        conditions = job.obj['status'].get('conditions') or []
        return any(True for c in conditions if c['type'] == 'Failed' and c['reason'] == 'DeadlineExceeded')

    def __job_failed_due_to_low_memory(self, job_state):
        """
        checks the state of the pod to see if it was killed
        for being out of memory (pod status OOMKilled). If that is the case
        marks the job for resubmission (resubmit logic is part of destinations).
        """

<<<<<<< HEAD
        pods = Pod.objects(self._pykube_api).filter(selector="app=" + job_state.job_id)
        pod = Pod(self._pykube_api, pods.response['items'][0])
=======
        pods = find_pod_object_by_name(self._pykube_api, job_state.job_id, self.runner_params['k8s_namespace'])
        if not pods.response['items']:
            return False
>>>>>>> refs/heads/release_21.01

        pod = Pod(self._pykube_api, pods.response['items'][0])
        if pod.obj['status']['phase'] == "Failed" and \
                pod.obj['status']['containerStatuses'][0]['state']['terminated']['reason'] == "OOMKilled":
            return True

        return False

    def fail_job(self, job_state):
        """
        Kubernetes runner overrides fail_job (called by mark_as_failed) to rescue the pod's log files which are left as
        stdout (pods logs are the natural stdout and stderr of the running processes inside the pods) and are
        deleted in the parent implementation as part of the failing the job process.

        :param job_state:
        :return:
        """

        # First we rescue the pods logs
        try:
            with open(job_state.output_file, 'r') as outfile:
                stdout_content = outfile.read()
        except IOError as e:
            stdout_content = "<Failed to recuperate log for job {} >".format(job_state.job_id)
            log.error("Failed to get stdout for job %s", job_state.job_id)
            log.exception(e)

        if getattr(job_state, 'stop_job', True):
            self.stop_job(job_state.job_wrapper)
        self._handle_runner_state('failure', job_state)
        # Not convinced this is the best way to indicate this state, but
        # something necessary
        if not job_state.runner_state_handled:
            job_state.job_wrapper.fail(
                message=getattr(job_state, 'fail_message', 'Job failed'),
                stdout=stdout_content, stderr='See stdout for pod\'s stderr.'
            )
            if job_state.job_wrapper.cleanup_job == "always":
                job_state.cleanup()

    def __produce_log_file(self, job_state):
        pod_r = Pod.objects(self._pykube_api).filter(selector="app=" + job_state.job_id)
        log_string = ""
        for pod_obj in pod_r.response['items']:
            try:
                pod = Pod(self._pykube_api, pod_obj)
                log_string += "\n\n==== Pod " + pod.name + " log start ====\n\n"
                log_string += pod.logs(timestamps=True)
                log_string += "\n\n==== Pod " + pod.name + " log end   ===="
            except Exception as detail:
                log.info("Could not write log file for pod %s due to HTTPError %s",
                         pod_obj['metadata']['name'], detail)
        if isinstance(log_string, text_type):
            log_string = log_string.encode('utf8')

        logs_file_path = job_state.output_file
        try:
            with open(logs_file_path, mode="w") as logs_file:
                logs_file.write(log_string)
        except IOError as e:
            log.error("Couldn't produce log files for %s", job_state.job_id)
            log.exception(e)

        return logs_file_path

    def stop_job(self, job_wrapper):
        """Attempts to delete a dispatched job to the k8s cluster"""
        job = job_wrapper.get_job()
        try:
            job_to_delete = find_job_object_by_name(self._pykube_api, job.get_job_runner_external_id(), self.runner_params['k8s_namespace'])
            if job_to_delete and len(job_to_delete.response['items']) > 0:
                k8s_job = Job(self._pykube_api, job_to_delete.response['items'][0])
                self.__cleanup_k8s_job(k8s_job)
            # TODO assert whether job parallelism == 0
            # assert not job_to_delete.exists(), "Could not delete job,"+job.job_runner_external_id+" it still exists"
            log.debug(f"({job.id}/{job.job_runner_external_id}) Terminated at user's request")
        except Exception as e:
            log.exception("({}/{}) User killed running job, but error encountered during termination: {}".format(
                job.id, job.get_job_runner_external_id(), e))

    def recover(self, job, job_wrapper):
        """Recovers jobs stuck in the queued/running state when Galaxy started"""
        # TODO this needs to be implemented to override unimplemented base method
        job_id = job.get_job_runner_external_id()
        log.debug("k8s trying to recover job: " + job_id)
        if job_id is None:
            self.put(job_wrapper)
            return
        ajs = AsynchronousJobState(files_dir=job_wrapper.working_directory, job_wrapper=job_wrapper)
        ajs.job_id = str(job_id)
        ajs.command_line = job.command_line
        ajs.job_wrapper = job_wrapper
        ajs.job_destination = job_wrapper.job_destination
        if job.state in (model.Job.states.RUNNING, model.Job.states.STOPPED):
            log.debug("({}/{}) is still in {} state, adding to the runner monitor queue".format(
                job.id, job.job_runner_external_id, job.state))
            ajs.old_state = model.Job.states.RUNNING
            ajs.running = True
            self.monitor_queue.put(ajs)
        elif job.state == model.Job.states.QUEUED:
            log.debug("({}/{}) is still in queued state, adding to the runner monitor queue".format(
                job.id, job.job_runner_external_id))
            ajs.old_state = model.Job.states.QUEUED
            ajs.running = False
            self.monitor_queue.put(ajs)

    def finish_job(self, job_state):
        super().finish_job(job_state)
        jobs = find_job_object_by_name(self._pykube_api, job_state.job_id, self.runner_params['k8s_namespace'])
        if len(jobs.response['items']) != 1:
            log.warning("More than one job matches selector. Possible configuration error"
                        " in job id '%s'", job_state.job_id)
        job = Job(self._pykube_api, jobs.response['items'][0])
        self.__cleanup_k8s_job(job)
