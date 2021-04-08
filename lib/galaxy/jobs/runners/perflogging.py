import json
import time

# AMP - gather job performance infomation
def job2json(job_wrapper, start=0, finish=None):
    j = job_wrapper
    if finish is None:
        finish = time.time()
    duration = finish - start    
    data = {
        'type': 'GALAXY JOB COMPLETE',        
        'start': start,
        'finish': finish,
        'duration': duration,
        'user': j.user,
        'session_id': j.get_session_id(),
        'workflow_invocation_uuid': j.get_param_dict().get('__workflow_invocation_uuid__', None),
        'id_tag': j.get_id_tag(),
        'state': j.get_state(),
        'sizes': j.get_output_sizes(),
        'tool_id': j.tool.id,
        'input_filenames': j.get_input_fnames(),
        'commandline': j.get_command_line(),
    }
    return json.dumps(data)
    

def queue2json(job_wrapper):
    j = job_wrapper
    data = {
        'type': 'GALAXY JOB QUEUE',
        'time': time.time(),
        'user': j.user,
        'session_id': j.get_session_id(),
        'workflow_invocation_uuid': j.get_param_dict().get('__workflow_invocation_uuid__', None),
        'id_tag': j.get_id_tag(),
    }
    return json.dumps(data)