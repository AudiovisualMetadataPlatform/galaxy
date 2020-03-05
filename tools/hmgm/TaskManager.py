from __builtin__ import True


class TaskManager:
     """Abstract base class defining the API for all HMGM task management implementations, which are based on task management platforms."""
     
     
     def __init__(self, root_dir):
         self.root_dir = root_dir

         # get HMGM configuration properties from the config file
         self.config = configparser.ConfigParser()
         self.config.read(root_dir + "/config/hmgm.ini")    
     
     
     def get_task_description(task_type, context, input_json, output_json):
         description = "Submitted By: " + context["submittedBy"] + "\n"
         description += "Unit " + context["unitId"] + ": " + context["unitName"] + "\n"
         description += "Collection  " + context["collectionId"] + ": " + context["collectionName"] + "\n"
         description += "Item " + context["itemId"] + ": " + context["itemName"] + "\n"
         description += "Primary File " + context["primaryfileId"] + ": " + context["primaryfileName"] + "\n"
         description += "Workflow " + context["workflowId"] + ": " + context["workflowName"] + "\n"
         description += "Workflow " + context["workflowId"] + ": " + context["workflowName"] + "\n"                  
         description += "Editor Tool: " + get_editor_link(task_type, context, input_json, output_json)          
         return description
     
     
     def get_editor_link(task_type, context, input_json, output_json):
         assert task_type in ("Transcript", "NER", "Segmentation", "OCR")
         
         if task_type == "Transcript":
             link = 
         
         return False
     

     def create_task(self, task_type, context, input_json, output_json, task_json):
         return None
     
     
     def close_task(self, task_json):
         return None