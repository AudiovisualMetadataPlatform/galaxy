class TaskJira (TaskManager):
     """Subclass of TaskManager implementing HMGM task management with OpenProject platforms."""
     
     def __init__(self, log_path):
         self.log_path = log_path
     
     def create_task(self, task_type, context, input_json, output_json, task_info):
         # TODO replace with real logic
         return None
     
     def close_task(self, task_info):
         # TODO replace with real logic
         return None