#!/usr/bin/env python3
import os
import os.path
import sys

# class HmgmBase:
#     """Abstract base class defining the API for all HMGM implementations, which are based on task management platforms."""

# Usage: hmgm_main.py [hmgm_type] [hmgm_log_path] [context] [input_json] [output_json] [hmgm_task] 
def main():
    (output_file) = sys.argv[1]
    try:
        if task_created() == False:
            create_task()
            exit(1) 
        else:
            if task_completed():
                close_task()
                write_output_file(output_file) # For testing only
                exit(0)
            else:
                exit(1)        
    except Exception as e:
        exit(-1)

# Return true if HMGM task already created, i.e. the file containing the HMGM task info exists
def task_created():
    return os.path.exists(argv[5])

def task_completed():
   
    return True