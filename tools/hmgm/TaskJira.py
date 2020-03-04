class TaskJira (TaskManager):
     """Subclass of TaskManager implementing HMGM task management with Jira platforms."""
     
     def __init__(self, log_path):
         self.log_path = log_path
     
     def create_task(self, task_type, context, input_json, output_json, task_info):
         # populate the jira fields into a dictionary with information from task_type and context etc
         project = {"key": "HMGM"}
         issuetype = {"name": "task"}
         labels = [task_type]
         summary = context["primaryfileName"] + " - " + context["workflowName"] 
         description = "Submitted By: " + context["submittedBy"] + "\n"
         description += "Unit " + context["unitId"] + ": " + context["unitName"] + "\n"
         description += "Collection  " + context["collectionId"] + ": " + context["collectionName"] + "\n"
         description += "Item " + context["itemId"] + ": " + context["itemName"] + "\n"
         description += "Primary File " + context["primaryfileId"] + ": " + context["primaryfileName"] + "\n"
         description += "Workflow " + context["workflowId"] + ": " + context["workflowName"] + "\n"
         description += "Workflow " + context["workflowId"] + ": " + context["workflowName"] + "\n"                  
         description += "Editor Tool: " + get_tool_link(task_type, context, input_json, output_json)          
         fields = {"project" : project, "issuetype": issuetype, "labels": labels, "summary": summary, "description": description}
         jira_json = {"fields": fields}
          
         # create a json file containing the jira info, needed by Jira creation REST API
         jira_path = self.log_path + "/" + "jira_create.json"
         with open(jira_path, "w") as jira_file: 
             json.dump(jira_json, jira_file) 
             
         # send REST request with the jira json file to HMGM jira server to create a jira
         
         
         return True
     
     def close_task(self, task_info):
         return True