"""
Job runner plugin for executing jobs on the local system via the command line.
"""
import datetime
import errno
import logging
import os
import subprocess
import tempfile
import threading
from time import sleep
from galaxy import model
from galaxy.jobs.runners import (
    AsynchronousJobRunner,
    AsynchronousJobState
)


from galaxy import model
from galaxy.util import (
    asbool,
    DATABASE_MAX_STRING_SIZE,
    shrink_stream_by_size
)
from ..runners import (
    BaseJobRunner,
    JobState
)

log = logging.getLogger(__name__)
stdout = ''
stderr = ''

DEFAULT_POOL_SLEEP_TIME = 5

class HmgmRunner(AsynchronousJobRunner):
    """
    Job runner backed by a finite pool of worker threads. FIFO scheduling
    """
    runner_name = "HmgmRunner"

    def __init__(self, app, nworkers):
        super(HmgmRunner, self).__init__(app, nworkers)
        self._init_monitor_thread()
        self._init_worker_threads()

    def queue_job(self, job_wrapper):
        log.debug("hmgmtest: queue job: " + job_wrapper.working_directory)
        self.prepare_job(job_wrapper)
        job_destination = job_wrapper.job_destination
        ajs = AsynchronousJobState(files_dir=job_wrapper.working_directory, job_wrapper=job_wrapper, job_id=job_wrapper.job_id, job_destination=job_destination)
        # Proceed with general initialization
        self.monitor_queue.put(ajs)

    # This is the main logic to determine what to do with thread.  Should it re-queue, be killed, or complete
    def check_watched_item(self, job_state):
        exit_code = self._run_job(job_state.job_wrapper)
        # This is a success code: The HMGM is complete
        if exit_code==0:
            job_state.running = False
            job_state.job_wrapper.change_state(model.Job.states.OK)
            self.mark_as_finished(job_state)
            try:
                # Write the output
                self.create_log_file(job_state, exit_code)
            except Exception:
                log.exception("Job wrapper finish method failed")
                self._fail_job_local(job_state.job_wrapper, "Unable to finish job")
            return None
        # This is a HMGM is not complete, try again later
        elif exit_code==1:
            job_state.running = False
            job_state.job_wrapper.change_state(model.Job.states.QUEUED)
            # Sleep the current thread.  Let's not iterate through too fast when re-queueing tasks
            sleep(DEFAULT_POOL_SLEEP_TIME)
            return job_state
        # Or we got an error
        else:
            job_state.running = False
            job_state.job_wrapper.change_state(model.Job.states.ERROR)
            return None

    # Copy stdout and stderr from process to files expected by job_state
    def create_log_file(self, job_state, exit_code):
        try:
            # Write stdout
            log_file = open(job_state.output_file, "w")
            log_file.write(self.stdout)
            log_file.close()
            
            # Write stderr
            log_file = open(job_state.error_file, "w")
            log_file.write(self.stderr)
            log_file.close()

            # Write exit code
            log_file = open(job_state.exit_code_file, "w")
            log_file.write(str(exit_code))
            log_file.close()

            log.debug("CREATE OUTPUT FILE: " + str(job_state.output_file))
            log.debug("CREATE ERROR FILE: " + str(job_state.error_file))
            log.debug("CREATE EXIT CODE FILE: " + str(job_state.exit_code_file))
        except IOError as e:
            log.error('Could not access task log file %s' % str(e))
            log.debug("IO Error occurred when accessing the files.")
            return False
        return True
    
    # This mostly copied out of runners/local.py - handle 
    def stop_job(self, job_wrapper):
        # if our local job has JobExternalOutputMetadata associated, then our primary job has to have already finished
        job = job_wrapper.get_job()
        job_ext_output_metadata = job.get_external_output_metadata()
        try:
            pid = job_ext_output_metadata[0].job_runner_external_pid  # every JobExternalOutputMetadata has a pid set, we just need to take from one of them
            assert pid not in [None, '']
        except Exception:
            # metadata internal or job not complete yet
            pid = job.get_job_runner_external_id()
        if pid in [None, '']:
            log.warning("stop_job(): %s: no PID in database for job, unable to stop" % job.id)
            return
        pid = int(pid)
        if not self._check_pid(pid):
            log.warning("stop_job(): %s: PID %d was already dead or can't be signaled" % (job.id, pid))
            return
        for sig in [15, 9]:
            try:
                os.killpg(pid, sig)
            except OSError as e:
                log.warning("stop_job(): %s: Got errno %s when attempting to signal %d to PID %d: %s" % (job.id, errno.errorcode[e.errno], sig, pid, e.strerror))
                return  # give up
            sleep(2)
            if not self._check_pid(pid):
                log.debug("stop_job(): %s: PID %d successfully killed with signal %d" % (job.id, pid, sig))
                return
        else:
            log.warning("stop_job(): %s: PID %d refuses to die after signaling TERM/KILL" % (job.id, pid))
    
    # Run job is a slightly modified version of run_job in runners/local.py.  It builds a command line proc
    # to execute, reads the stdout and stderr, and returns the status
    def _run_job(self, job_wrapper):
        exit_code = 0

        # command line has been added to the wrapper by prepare_job()
        command_line, exit_code_path = self.__command_line(job_wrapper)
        job_id = job_wrapper.get_id_tag()

        try:
            stdout_file = tempfile.NamedTemporaryFile(mode='wb+', suffix='_stdout', dir=job_wrapper.working_directory)
            stderr_file = tempfile.NamedTemporaryFile(mode='wb+', suffix='_stderr', dir=job_wrapper.working_directory)
            log.debug('(%s) executing job script: %s' % (job_id, command_line))

            proc = subprocess.Popen(args=command_line,
                                    shell=True,
                                    cwd=job_wrapper.working_directory,
                                    stdout=stdout_file,
                                    stderr=stderr_file,
                                    preexec_fn=os.setpgrp)

            proc.terminated_by_shutdown = False

            try:
                job_wrapper.set_job_destination(job_wrapper.job_destination, proc.pid)
                job_wrapper.change_state(model.Job.states.RUNNING)

                # Reap the process and get the exit code.
                exit_code = proc.wait()
                                  
            except Exception:
                log.warning("Failed to read exit code from process")

            try:
                exit_code = int(open(exit_code_path, 'r').read())                    
            except Exception:
                log.warning("Failed to read exit code from path %s" % exit_code_path)
                

            if proc.terminated_by_shutdown:
                self._fail_job_local(job_wrapper, "job terminated by Galaxy shutdown")
                return -1

            stdout_file.seek(0)
            stderr_file.seek(0)
            self.stdout = shrink_stream_by_size(stdout_file, DATABASE_MAX_STRING_SIZE, join_by="\n..\n", left_larger=True, beginning_on_size_error=True)
            self.stderr = shrink_stream_by_size(stderr_file, DATABASE_MAX_STRING_SIZE, join_by="\n..\n", left_larger=True, beginning_on_size_error=True)
            stdout_file.close()
            stderr_file.close()
            log.debug('execution finished: %s' % command_line)
        except Exception:
            log.exception("failure running job %d", job_wrapper.job_id)
            self._fail_job_local(job_wrapper, "failure running job")
            return -1
        
        return exit_code

    # Copied from runners/local.py
    def _fail_job_local(self, job_wrapper, message):
        job_destination = job_wrapper.job_destination
        job_state = JobState(job_wrapper, job_destination)
        job_state.fail_message = message
        job_state.stop_job = False
        self.fail_job(job_state, exception=True)

    # Copied from runners/local.py
    def __command_line(self, job_wrapper):
        """
        """
        command_line = job_wrapper.runner_command_line

        # slots would be cleaner name, but don't want deployers to see examples and think it
        # is going to work with other job runners.
        slots_statement = 'GALAXY_SLOTS="1"; export GALAXY_SLOTS;'

        job_id = job_wrapper.get_id_tag()
        job_file = JobState.default_job_file(job_wrapper.working_directory, job_id)
        exit_code_path = JobState.default_exit_code_file(job_wrapper.working_directory, job_id)
        job_script_props = {
            'slots_statement': slots_statement,
            'command': command_line,
            'exit_code_path': exit_code_path,
            'working_directory': job_wrapper.working_directory,
        }
        job_file_contents = self.get_job_file(job_wrapper, **job_script_props)
        self.write_executable_script(job_file, job_file_contents)
        return job_file, exit_code_path
    
    # Copied from runners/local.py
    def _check_pid(self, pid):
        try:
            os.kill(pid, 0)
            return True
        except OSError as e:
            if e.errno == errno.ESRCH:
                log.debug("_check_pid(): PID %d is dead" % pid)
            else:
                log.warning("_check_pid(): Got errno %s when attempting to check PID %d: %s" % (errno.errorcode[e.errno], pid, e.strerror))
            return False