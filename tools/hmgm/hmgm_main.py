#!/usr/bin/env python3
import os
import os.path
import sys
import json

# class HmgmBase:
#     """Abstract base class defining the API for all HMGM implementations, which are based on task management platforms."""


# Usage: hmgm_main.py task_type root_dir context_json input_json output_json task_json 
def main():
    # parse command line arguments
    task_type = sys.argv[1]     # type of HMGM task: (Transcript, NER, Segmentation, OCR), there is one HMGM wrapper per type
    root_dir = sys.argv[2]      # path for Galaxy root directory; HMGM property files, logs and tmp files are relative to the root_dir
    context_json = sys.argv[3]  # context info needed for creating HMGM tasks
    input_json = sys.argv[4]    # input file for HMGM task in json format
    output_json = sys.argv[5]   # output file for HMGM task in json format
    task_json = sys.argv[6]     # file storing information about the HMGM task, such as ticket # etc

    try:
        if not task_created(task_json):
            create_task(task_type, root_dir, context_json, input_json, output_json, task_json)
            exit(1) 
        elif task_completed(output_json):
            close_task(context_json, task_json)
            exit(0)
        else:
             exit(1)        
    except Exception as e:
        exit(-1)


# Return true if HMGM task has already been created, i.e. the file containing the HMGM task info exists.
def task_created(task_json):
    return os.path.exists(task_json)


# Return true if HMGM task has already been completed, i.e. the output JSON file exists.
def task_completed(output_json):   
    return os.path.exists(output_json)


# Create an HMGM task in the specified task management platform with the given context, and input/output files, 
# save information about the created task into a json file, and return the created task.
def create_task(task_type, root_dir, context_json, input_json, output_json, task_json):
    # get task management instance based on task platform specified in context
    taskManager = get_task_manager(root_dir, context_json)
    
    # calling task manager API to create task in the corresponding platform
    return taskManager.create_task(task_type, context, input_json, output_json, task_json)
    
    
# Close the HMGM task specified in the task information file in the corresponding task mamangement platform.
def close_task(context_json, task_json):
    # get task management instance based on task platform specified in context
    taskManager = get_task_manager(root_dir, context_json)
    
    # calling task manager API to close task in the corresponding platform
    return taskManager.close_task(task_json)
    
    
# Create subclass of task manager instance based on task platform specified in the given context.
def get_task_manager(root_dir, context_json):
    context = json.loads(context_json)
    manager = context["taskManager"]
    assert manager in ("Jira", "OpenProject", "Redmine")
    
    # create subclass of task instance based on task platform specified in context
    if manager == "Jira":
        taskManager = TaskJira(root_dir)
    elif manager == "OpenProject":
        taskManager = TaskOpenproject(root_dir)
    elif manager == "Redmine":
        taskManager = TaskRedmine(root_dir)            
    return taskManager


if __name__ == "__main__":
    main()    