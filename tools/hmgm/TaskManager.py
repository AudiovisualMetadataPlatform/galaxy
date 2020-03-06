from __builtin__ import True
import configparser

class TaskManager:
     """Abstract base class defining the API for all HMGM task management implementations, which are based on task management platforms."""
     
     
     # Set up configuration instance with properties in the HMGM config file
     def __init__(self, root_dir):
         self.root_dir = root_dir

         # get amppd HMGM configuration properties from the config file
         self.config = configparser.ConfigParser()
         self.config.read(root_dir + "/config/hmgm.ini")    
         self.amppd_server = self.config["amppd"]["server"] 
         self.transcript_api = self.config["amppd"]["transcript_api"] 
         self.transcript_input = self.config["amppd"]["transcript_input"] 
         self.transcript_output = self.config["amppd"]["transcript_output"] 
         self.transcript_media = self.config["amppd"]["transcript_media"] 
         
     
     # Return description of an HMGM task based on the given task_type, context, input/output files etc.
     def get_task_description(self, task_type, context, input_json, output_json):
         description = "Submitted By: " + context["submittedBy"] + "\n"
         description += "Unit " + context["unitId"] + ": " + context["unitName"] + "\n"
         description += "Collection  " + context["collectionId"] + ": " + context["collectionName"] + "\n"
         description += "Item " + context["itemId"] + ": " + context["itemName"] + "\n"
         description += "Primary File " + context["primaryfileId"] + ": " + context["primaryfileName"] + "\n"
         description += "Workflow " + context["workflowId"] + ": " + context["workflowName"] + "\n"
         description += "Workflow " + context["workflowId"] + ": " + context["workflowName"] + "\n"                  
         description += "Editor Tool: " + get_editor_url(task_type, context["primaryfileUrl"], input_json, output_json)          
         return description
     
     
     # Return the URL link to the editor tool for an HMGM task based on the given task_type, media, input/output files etc.
     def get_editor_url(self, task_type, media, input_json, output_json):
         assert task_type in ("Transcript", "NER", "Segmentation", "OCR")
         
         if task_type == "Transcript":
             url = self.amppd_server + self.transcript_api 
             url += "?" + self.transcript_input + "=" + input_json
             url += "&" + self.transcript_output + "=" + output_json
             url += "&" + self.transcript_media + "=" + media
         elif task_type == "NER":
             # TODO url for NER
             url = self.amppd_server;
         elif task_type == "Segmentation":
             # TODO url for NER
             url = self.amppd_server;
         elif task_type == "NEROCR":
             # TODO url for NER
             url = self.amppd_server;

         return url
     

     # Abstract method to create a task in the designated task management platform, given the task_type, context, input/output files etc. 
     # save information about the created task into a json file, and return the task instance.
     def create_task(self, task_type, context, input_json, output_json, task_json):
         return None
     
     
     # Abstract method to close the task specified in task_json by updating its status and relevant fields, and return the task instance.          
     def close_task(self, task_json):
         return None