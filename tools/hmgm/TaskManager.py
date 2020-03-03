from __builtin__ import True
class TaskManager:
     """Abstract base class defining the API for all HMGM task management implementations, which are based on task management platforms."""
     
     def __init__(self, log_path):
         self.log_path = log_path
     
     def create_task(self, task_type, context, input_json, output_json, task_info):
         return None
     
     def close_task(self, task_info):
         return None