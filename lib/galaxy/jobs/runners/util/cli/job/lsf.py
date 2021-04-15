# A simple CLI runner for slurm that can be used when running Galaxy from a
# non-submit host and using a Slurm cluster.
from logging import getLogger
from os import path

<<<<<<< HEAD
try:
    from galaxy.model import Job
    job_states = Job.states
except ImportError:
    # Not in Galaxy, map Galaxy job states to Pulsar ones.
    from pulsar.util import enum
    job_states = enum(RUNNING='running', OK='complete', QUEUED='queued', ERROR="failed")

from ..job import BaseJobExec
=======
from galaxy.jobs import JobState
from ..job import BaseJobExec, job_states
>>>>>>> refs/heads/release_21.01

log = getLogger(__name__)

argmap = {
    'memory': '-M',  # There is code in job_script_kwargs relying on this name's setting
    'cores': '-n',
    'queue': '-q',
    'working_dir': '-cwd'
}


class LSF(BaseJobExec):

    def __init__(self, **params):
        self.params = {}
        for k, v in params.items():
            self.params[k] = v

    def job_script_kwargs(self, ofile, efile, job_name):
        scriptargs = {'-o': ofile,
                      '-e': efile,
                      '-J': job_name}

        # Map arguments using argmap.
        for k, v in self.params.items():
            if k == 'plugin' or k == 'excluded_hosts':
                continue
            try:
                if k == 'memory':
                    # Memory requires both -m and -R rusage[mem=v] request
                    scriptargs['-R'] = "\"rusage[mem=%s]\"" % v
                if not k.startswith('-'):
                    k = argmap[k]
                scriptargs[k] = v
            except Exception:
                log.warning('Unrecognized long argument passed to LSF CLI plugin: %s' % k)

        # Generated template.
        template_scriptargs = ''
        for k, v in scriptargs.items():
            template_scriptargs += f'#BSUB {k} {v}\n'
        # Excluded hosts use the same -R option already in use for mem, so easier adding here.
        for host in self._get_excluded_hosts():
            template_scriptargs += f'#BSUB -R \"select[hname!=\'{host}\']\"\n'
        return dict(headers=template_scriptargs)

    def submit(self, script_file):
        # bsub returns Job <9147983> is submitted to default queue <research-rh7>.
        # This should be really handled outside with something like
        # parse_external. Currently CLI runner expect this to just send it in the last position
        # of the string.
        return "bsub <%s | awk '{ print $2}' | sed 's/[<>]//g'" % script_file

    def delete(self, job_id):
        return 'bkill %s' % job_id

    def get_status(self, job_ids=None):
        return "bjobs -a -o \"id stat\" -noheader"  # check this

    def get_single_status(self, job_id):
        return "bjobs -o stat -noheader " + job_id

    def parse_status(self, status, job_ids):
        # Get status for each job, skipping header.
        rval = {}
        for line in status.splitlines():
            job_id, state = line.split()
            if job_id in job_ids:
                # map job states to Galaxy job states.
                rval[job_id] = self._get_job_state(state)
        return rval

    def parse_single_status(self, status, job_id):
        if not status:
            # Job not found in LSF, most probably finished and forgotten.
            # lsf outputs: Job <num> is not found -- but that is on the stderr
            # Note: a very old failed job job will not be shown here either,
            # which would be badly handled here. So this only works well when Galaxy
            # is constantly monitoring the jobs. The logic here is that DONE jobs get forgotten
            # faster than failed jobs.
            log.warning("Job id '%s' not found LSF status check" % job_id)
            return job_states.OK
        return self._get_job_state(status)

    def _get_job_state(self, state):
        # based on:
        # https://www.ibm.com/support/knowledgecenter/en/SSETD4_9.1.3/lsf_admin/job_state_lsf.html
        # https://www.ibm.com/support/knowledgecenter/en/SSETD4_9.1.2/lsf_command_ref/bjobs.1.html
        try:
            return {
                'EXIT': job_states.ERROR,
                'RUN': job_states.RUNNING,
                'PEND': job_states.QUEUED,
                'DONE': job_states.OK,
                'PSUSP': job_states.ERROR,
                'USUSP': job_states.ERROR,
                'SSUSP': job_states.ERROR,
                'UNKWN': job_states.ERROR,
                'WAIT': job_states.QUEUED,
                'ZOMBI': job_states.ERROR
            }.get(state)
        except KeyError:
            raise KeyError("Failed to map LSF status code [%s] to job state." % state)

    def _get_excluded_hosts(self):
        """
        Reads a file in the set path with one node name per line. All these nodes will be added
        to the exclusion list for execution.

        The path can be added to destinations like this:

        <destination id="lsf_8cpu_16GbRam" runner="cli">
            <param id="shell_plugin">LocalShell</param>
            <param id="job_plugin">LSF</param>
            <param id="job_memory">16000</param>
            <param id="job_cores">7</param>
            <param id="job_excluded_hosts">/path/to/file/with/hosts/to/exclude/one/per/line.txt</param>
        </destination>

        :param pathExcludedNodes:
        :return: list with node names
        """
        if "excluded_hosts" in self.params:
            path_excluded = self.params["excluded_hosts"]
            if path.isfile(path_excluded):
                with open(path_excluded) as f:
                    return f.read().splitlines()
        return []


__all__ = ('LSF',)
