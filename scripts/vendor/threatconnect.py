"""
Module for transforming ThreatConnect playbooks.
"""

import json

class ThreatConnect():
    """
    A playbook transformation class. Converts ThreatConnect-specific playbooks into a JSON schema.
    """

    def __init__(self, filename: str):
            self.filename = filename

    def getDictionary(self,json_object, my_dict={}):
        def iterateDict(json_object, my_dict={}):
            try:
                for k,v in dict(json_object).items():

                    # if values are a list
                    if isinstance(v, list):

                        # if list has only one entry, e.g., key : []
                        if len(v) == 0:
                            if k not in my_dict:
                                my_dict[k] = {}

                        # if list contains only one key, e.g., key : ['brandinstances']
                        elif len(v) == 1:
                            my_dict[k] = {}
                            my_dict[k] = iterateDict(v[0], my_dict[k])

                        # if the list contains one nested list, e.g., key: [[]]
                        elif isinstance(v[0], list) and k not in my_dict and len(v[0]) == 1:
                            my_dict[k] = iterateDict(v[0][0])

                        # if the nested object is a dictionary, e.g., key : [{}]
                        elif isinstance(v[0], dict) and k not in my_dict:
                            my_dict[k] = {}
                            my_dict[k] = iterateDict(v[0], my_dict[k])

                        # if the list contains multiple dictionaries [{},{},{}] or lists [[],[],[]]
                        else:
                            if k not in my_dict:
                                my_dict[k] = {}
                            for i in v:
                                if isinstance(i, str): 
                                    my_dict[k] = i
                                elif isinstance(i, list) and len(i) == 1:
                                    my_dict[k] = iterateDict(i[0], my_dict[k])
                                else:
                                    my_dict[k] = iterateDict(i, my_dict[k])
                    else:
                        # HERE IS THE MAIN DIFFERENCE FOR EACH VENDOR
                        if isinstance(v, dict):
                            if k not in my_dict:
                                my_dict[k] = {}
                            my_dict[k] = iterateDict(v,my_dict[k])
                        elif k not in my_dict:
                            my_dict[k] = v 
            except:
                raise

            return my_dict
        return iterateDict(json_object,my_dict)


    #@file_handler
    def mapValues(self, dict={}):
        try:
            with open(self.filename, 'r', encoding='utf-8') as yaml_file:
                playbook_json = json.load(yaml_file)
                return self.getDictionary(playbook_json, dict) 
        except:
            raise

    def analyze_playbook(self, analysis_dict):
        try:
            with open(self.filename, 'r', encoding='utf-8') as yaml_file:
                playbook_json = json.load(yaml_file)

                steps = playbook_json["jobList"]
                tags = [] 
                if "playbooksLabels" in playbook_json:
                    if len(playbook_json["playbooksLabels"]) != 0:
                        for label in playbook_json["playbookLabels"]:
                            tags.append(label["playbookLabelType"]["label"])


                name = playbook_json["name"]
                description = ""
                if "description" in playbook_json:
                    description = playbook_json["description"].replace("\n", " ").replace("\r", " ")

                # vendor
                if "vendor" not in analysis_dict:
                    analysis_dict["vendor"] = []
                analysis_dict["vendor"].append("ThreatConnect")

                # actuator
                if "actuator" not in analysis_dict:
                     analysis_dict["actuator"] = []
                actuator = []
                for task in steps:
                    if "appCatalogItem" in task:
                        if "TCPB" in task["appCatalogItem"]["programName"]:
                            actuator_task = task["appCatalogItem"]["programName"].split(" - ")[1].split(" ")[:-1]
                            actuator_task = " ".join(actuator_task)
                            actuator.append(actuator_task)
                        else:
                            actuator.append("")
                    else:
                        actuator.append("")
                analysis_dict["actuator"].append(actuator)

                # tags
                if "tags" not in analysis_dict:
                    analysis_dict["tags"] = []
                tags = []
                for tag in tags:
                    tags.append(tag)
                analysis_dict["tags"].append(tags)       


                # get number of steps
                if "steps" not in analysis_dict:
                    analysis_dict["steps"] = []
                analysis_dict["steps"].append(len(steps))

                # get the step types
                if "step_types" not in analysis_dict:
                     analysis_dict["step_types"] = []
                step_types = []
                for step in steps:
                    step_types.append("")
                analysis_dict["step_types"].append(step_types)

                # get the step names
                if "step_names" not in analysis_dict:
                     analysis_dict["step_names"] = []
                step_names = []
                for step in steps:
                    step_names.append(str(step["name"]))
                analysis_dict["step_names"].append(step_names)

                # playbook name
                if "playbook_name" not in analysis_dict:
                    analysis_dict["playbook_name"] = []
                analysis_dict["playbook_name"].append(name)
                
                # playbook description
                if "playbook_description" not in analysis_dict:
                    analysis_dict["playbook_description"] = []
                analysis_dict["playbook_description"].append(description)

                return analysis_dict

        except:
            raise