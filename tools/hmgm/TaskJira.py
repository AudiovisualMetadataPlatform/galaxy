class TaskJira (TaskManager):
     """Subclass of TaskManager implementing HMGM task management with Jira platforms."""
     
     def __init__(self, log_path):
         self.log_path = log_path
     
     def create_task(self, task_type, context, input_json, output_json, task_info):
         # populate the jira fields into a dictionary with information from task_type and context etc
         jira_fields = {}
         jira['project'] = 
          
         # create a json file needed by Jira creation REST API
         
         return True
     
     def close_task(self, task_info):
         return True