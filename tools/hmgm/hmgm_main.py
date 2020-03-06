#!/usr/bin/env python3
import json
import os
import os.path
import sys
import shutil
import configparser

# It's assumed that all HMGMs generate the output file in the same directory as the input file with ".completed" suffix added to the original filename
HMGM_OUTPUT_SUFFIX = ".complete"

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
#         elif task_completed(output_json):
        else:
            output_path = task_completed(input_json)
            if (output_path):
                close_task(root_dir, context_json, output_path, output_json, task_json)
                exit(0)
            else:
                exit(1)        
    except Exception as e:
        exit(-1)


# Return true if HMGM task has already been created, i.e. the file containing the HMGM task info exists.
def task_created(task_json):
    return os.path.exists(task_json)


# If HMGM task has already been completed, i.e. the output JSON file exists, return the output file path; otherwise return False. 
def task_completed(input_json):   
    output_path = get_editor_input_path(input_json) + HMGM_OUTPUT_SUFFIX
    if os.path.exists(output_path):
        return output_path
    else:
        return False


# # Return true if HMGM task has already been completed, i.e. the output JSON file exists.
# def task_completed(output_json):   
#     return os.path.exists(output_json)


# Create an HMGM task in the specified task management platform with the given context, and input/output files, 
# save information about the created task into a json file, and return the created task.
def create_task(task_type, root_dir, context_json, input_json, output_json, task_json):
    # set up the input file in the designated location for HMGM task editor to pick up
    setup_editor_input_file(input_json)
    
    # get task management instance based on task platform specified in context
    taskManager = get_task_manager(root_dir, context_json)
    
    # calling task manager API to create task in the corresponding platform
    return taskManager.create_task(task_type, context, input_json, output_json, task_json)
    
    
# Close the HMGM task specified in the task information file in the corresponding task mamangement platform.
def close_task(root_dir, context_json, output_path, output_json, task_json):
    # set up the output file dropped by HMGM task editor in the designated location
    cleanup_editor_output_file(output_path, output_json)
    
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


# Derive the input json file path for HMGM tool editor, based on the given input json file passed in from the corresponding Galaxy job. 
def get_editor_input_path(input_json):
    # Note: 
    # The reason we don't pass the original Galaxy input_json path to HMGM task tools is that we want to avoid exposing the internal Galaxy file system to external apps; 
    # for security concerns. Instead, we can use a designated directory for passing input/output files, and generate a soft link in (or copy the file to) this 
    # directory, using a filename unique mapped from the original filename. 

    config = configparser.ConfigParser()
    config.read(root_dir + "/config/hmgm.ini")    
    io_dir = config["amppd"]["io_dir"] 

    # TODO replace below code with logic to generate an obscure soft link based on the original file path
    # for now we just use the original filename within the designated directory
    filename = os.path.basename(input_json)
    filepath = io_dir + "/" + filename
    
    return filepath
     
# Set up the input file of the given input json in the designated location for the HMGM editor to pick up.     
def setup_editor_input_file(input_json):     
    # TODO update logic here as needed to generate an obscure soft link instead of copying
    # for now lets copy the file
    input_path = get_editor_input_path(input_json)
    shutil.copy(input_json, input_path)
#     os.symlink(input_json, input_path)
    return input_path


# Clean up the output file dropped by HMGM task editor for the given input json by moving it from the designated location to the output file expected by Galaxy job;
# also, (optionally) clean up the corresponding input file in that directory, and return the input file path.
def cleanup_editor_output_file(output_path, output_json):     
    # move the completed output file to the location expected by Galaxy
    shutil.move(output_path, output_json)

    # TODO decide if it's better to remove the input file here or do it in a batch process
    input_path = output_path[:-len(HMGM_OUTPUT_SUFFIX)]
    
    return input_path


if __name__ == "__main__":
    main()    