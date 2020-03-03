#!/usr/bin/env python3
import os
import os.path
import sys
import json

# class HmgmBase:
#     """Abstract base class defining the API for all HMGM implementations, which are based on task management platforms."""

# Usage: hmgm_main.py task_type log_path context_json input_json output_json task_info 
def main():
    # parse command line arguments
    task_type = sys.argv[1]     # type of HMGM task: (TRANSCRIPT, NER, SEGMENTATION), there is one HMGM wrapper per type
    log_path = sys.argv[2]      # path for HMGM logs and tmp files
    context_json = sys.argv[3]  # context info needed for creating HMGM tasks
    input_json = sys.argv[4]    # input file for HMGM task in json format
    output_json = sys.argv[5]   # output file for HMGM task in json format
    task_info = sys.argv[6]     # file storing information about the HMGM task, such as ticket # etc

    try:
        if not task_created(task_info):
            create_task(task_type, log_path, context_json, input_json, output_json, task_info)
            exit(1) 
        elif task_completed(output_json):
            close_task(context_json, task_info)
            exit(0)
        else:
             exit(1)        
    except Exception as e:
        exit(-1)

# Return true if HMGM task has already been created, i.e. the file containing the HMGM task info exists.
def task_created(task_info):
    return os.path.exists(task_info)

# Return true if HMGM task has already been completed, i.e. the output JSON file exists.
def task_completed(output_json):   
    return os.path.exists(output_json)

def create_task(task_type, log_path, context_json, input_json, output_json, task_info):
    # get task management instance based on task platform specified in context
    taskManager = get_task_manager(log_path, context_json)
    # calling task manager API to create task in the corresponding platform
    return taskManager.create_task(task_type, context, input_json, output_json, task_info)
    
def close_task(context_json, task_info):
    # get task management instance based on task platform specified in context
    taskManager = get_task_manager(log_path, context_json)
    # calling task manager API to close task in the corresponding platform
    return taskManager.close_task(task_info)
    
# Create subclass of task instance based on task platform specified in the given context.
def get_task_manager(log_path, context_json):
    context = json.loads(context_json)
    manager = context['taskManager']
    assert manager in ('JIRA', 'OPENPROJECT', 'REDMINE')
    # create subclass of task instance based on task platform specified in context
    if manager == 'JIRA':
        taskManager = TaskJira(task_type, log_path, context_json, input_json, output_json, task_info)
    elif manager == 'OPENPROJECT':
        taskManager = TaskOpenproject(task_type, log_path, context_json, input_json, output_json, task_info)
    elif manager == 'REDMINE':
        taskManager = TaskRedmine(task_type, log_path, context_json, input_json, output_json, task_info)            
    return taskManager

if __name__ == "__main__":
    main()    