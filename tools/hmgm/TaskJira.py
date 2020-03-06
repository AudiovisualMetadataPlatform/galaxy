from jira import JIRA

 
class TaskJira (TaskManager):
     """Subclass of TaskManager implementing HMGM task management with Jira platforms."""
     
     
     # Set up jira instance with properties in the given configuration instance.
     def __init__(self, config):
#          self.root_dir = root_dir
#          self.config = configparser.ConfigParser()
#          self.config.read(root_dir + "/config/hmgm.ini")    
#          super().__init__(root_dir)
         super().__init__(config)
         
         # get Jira server info from the config 
         jira_server = config["jira"]["server"]
         jira_username = config["jira"]["username"]
         jira_password = config["jira"]["password"]         
         self.jira = JIRA(server = jira_server, basic_auth = (jira_username, jira_password))
         
         
     # Create a jira issue given the task_type, context, input/output json, 
     # save information about the created issue into a JSON file, and return the issue.
     def create_task(self, task_type, context, input_path, task_json):
         # populate the jira fields into a dictionary with information from task_type and context etc
         project = {"key": "HMGM"}
         issuetype = {"name": "Task"}
         labels = [task_type]
         summary = context["primaryfileName"] + " - " + context["workflowName"] 
         description = get_task_description(task_type, context, input_path)         
         jira_fields = {"project" : project, "issuetype": issuetype, "labels": labels, "summary": summary, "description": description}
         
         # create a new task jira using jira module
         issue = self.jira.create_issue(fields = jira_fields)
         
         # extract important information (ID, key, and URL) of the created issue into a dictionary, which is essentially the response returned by Jira server
         issue_dict = {"id": issue.id, "key": issue.key, "url": issue.permalink()} 

         # write jira issue into task_json file to indicate successful creation of the task
         json.dump(issue_dict, task_json)
         
#          jira_json = {"fields": fields}          
#          # create a json file containing the jira info, needed by Jira creation REST API
#          jira_path = self.log_path + "/" + "jira_create.json"
#          with open(jira_path, "w") as jira_file: 
#              json.dump(jira_json, jira_file) 
#              
#          # send REST request with the jira json file to HMGM jira server to create a jira
                  
         return issue
     
          
     # Close the jira issue specified in task_json by updating its status and relevant fields, and return the issue.          
     def close_task(self, task_json):
         # read jira issue info from task_json into a dictionary
         issue_dict = json.loads(task_json)
         
         # get the jira issue using id
         issue = self.jira.issue(issue_dict["id"])
         
         # retrieve transition ID based on name = Done instead of hard coding it, if the ID might be different
         transitions = jira.transitions(issue)
         for t in transitions:
             if t["name"] == "Done":    # Done is the status when an issue is closed
                 id = t["id"]
                 break
             
         # update the jira status to Done via transition
         self.jira.transition_issue(issue, id)
                  
         return issue
     
     