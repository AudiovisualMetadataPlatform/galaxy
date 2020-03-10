#!/usr/bin/env python3

import configparser
import json
import os
import os.path
import sys
import shutil

from task_jira import TaskJira
from task_openproject import TaskOpenproject 
from task_redmine import TaskRedmine


# It's assumed that all HMGMs generate the output file in the same directory as the input file with ".completed" suffix added to the original filename
HMGM_OUTPUT_SUFFIX = ".complete"
JIRA = "Jira"
OPEN_PROJECT = "OpenProject"
REDMINE = "Redmine"


# Usage: hmgm_main.py task_type root_dir context_json input_json output_json task_json 
def main():
    # parse command line arguments
    task_type = sys.argv[1]     # type of HMGM task: (Transcript, NER, Segmentation, OCR), there is one HMGM wrapper per type
    root_dir = sys.argv[2]      # path for Galaxy root directory; HMGM property files, logs and tmp files are relative to the root_dir
    input_json = sys.argv[3]    # input file for HMGM task in json format
    output_json = sys.argv[4]   # output file for HMGM task in json format
    task_json = sys.argv[5]     # json file storing information about the HMGM task, such as ticket # etc
    context_json = sys.argv[6]  # context info as json string needed for creating HMGM tasks

    try:
        config = config_hmgm(root_dir);
        context = json.loads(context_json)

        if not task_created(task_json):
            task = create_task(config, task_type, context, input_json, output_json, task_json)
            print ("Successfully created HMGM task " + task)
            exit(1) 
        else:
            output_path = task_completed(config, input_json)
            if (output_path):
                task = close_task(config, context, output_path, output_json, task_json)
                print ("Successfully closed HMGM task " + task)
                exit(0)
            else:
                print ("Waiting for HMGM task to complete ...")
                exit(1)        
    except Exception as e:
        print ("Exception while handling HMGM task: " + e.message)
        exit(-1)


# Load basic HGMG configuration based from the property file under the given root directory and return the configuration instance.
def config_hmgm(root_dir):
    config = configparser.ConfigParser()
    config.read(root_dir + "/config/hmgm.ini")    
    return config

 
# Return true if HMGM task has already been created, i.e. the file containing the HMGM task info exists.
def task_created(task_json):
    return os.path.exists(task_json)


# If HMGM task has already been completed, i.e. the output JSON file for the given input JSON file exists, return the output file path; otherwise return False. 
def task_completed(config, input_json):   
    output_path = get_editor_input_path(config, input_json) + HMGM_OUTPUT_SUFFIX
    if os.path.exists(output_path):
        return output_path
    else:
        return False


# # Return true if HMGM task has already been completed, i.e. the output JSON file exists.
# def task_completed(output_json):   
#     return os.path.exists(output_json)


# Create an HMGM task in the specified task management platform with the given context and input/output files, 
# save information about the created task into a JSON file, and return the created task.
def create_task(config, task_type, context, input_json, output_json, task_json):
    # set up the input file in the designated location for HMGM task editor to pick up
    input_path = setup_editor_input_file(config, input_json)
    
    # get task management instance based on task platform specified in context
    taskManager = get_task_manager(config, context)
    
    # calling task manager API to create task in the corresponding platform
    return taskManager.create_task(task_type, context, input_path, task_json)
    
    
# Close the HMGM task specified in the task information file in the corresponding task mamangement platform.
def close_task(config, context, output_path, output_json, task_json):
    # clean up the output file dropped by HMGM task editor in the designated location
    cleanup_editor_output_file(output_path, output_json)
    
    # get task management instance based on task platform specified in context
    taskManager = get_task_manager(config, context)
    
    # calling task manager API to close task in the corresponding platform
    return taskManager.close_task(task_json)
    
    
# Set up the input file corresponding to the given input JSON file in the designated location for HMGM editors to pick up.     
def setup_editor_input_file(config, input_json):     
    # TODO update logic here as needed to generate an obscure soft link instead of copying
    input_path = get_editor_input_path(config, input_json)
    shutil.copy(input_json, input_path)
#     os.symlink(input_json, input_path)
    return input_path


# Clean up the output file dropped by HMGM task editors by moving it from the designated location to the output file expected by Galaxy job;
# also, (optionally) remove the corresponding input file in that directory, and return the input file path.
def cleanup_editor_output_file(output_path, output_json):     
    # move the completed output file to the location expected by Galaxy
    shutil.move(output_path, output_json)

    # TODO decide if it's better to remove the input file here or do it in a batch process
    input_path = output_path[:-len(HMGM_OUTPUT_SUFFIX)]
    os.remove(input_path)
    
    return input_path

    
# Derive the input file path used by HMGM tool editors for the given input JSON file passed in from the corresponding Galaxy job. 
def get_editor_input_path(config, input_json):
    # Note: 
    # For security concerns, we don't pass the original input path to HMGM task editors, to avoid exposing the internal Galaxy file system to external web apps; 
    # Instead, we use a designated directory for passing such input/output files, and generate a soft link in (or copy the file to) this directory, 
    # using a filename uniquely mapped from the original filename.  
    io_dir = config["amppd"]["io_dir"] 

    # TODO replace below code with logic to generate an obscure soft link based on the original file path
    # for now we just use the original filename within the designated directory
    filename = os.path.basename(input_json)
    filepath = io_dir + "/" + filename
    
    return filepath
     
    
# Create subclass of task manager instance based on task platform specified in the given context.
def get_task_manager(config, context):
    manager = context["taskManager"]
    assert manager in (JIRA, OPEN_PROJECT, REDMINE)
    
    # create subclass of task instance based on task platform specified in context
    if manager == JIRA:
        taskManager = TaskJira(config)
    elif manager == OPEN_PROJECT:
        taskManager = TaskOpenproject(config)
    elif manager == REDMINE:
        taskManager = TaskRedmine(config)            
    return taskManager


if __name__ == "__main__":
    main()    