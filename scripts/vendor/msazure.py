"""
Module for transforming MSAzure playbooks.
"""

import json
import re

class MSAzure():
    """
    A playbook transformation class. Converts MSAzure-specific playbooks into a JSON schema.
    """

    def __init__(self, filename: str):
        """
        Initializes the class with the given filename.

        Args:
        - filename (str): The name of the file to be processed.
        """
        self.filename = filename

    def get_dictionary(self, json_object, my_dict={}) -> dict:
        """
        Converts a JSON object to a dictionary.

        Args:
        - json_object (dict): A JSON object to be converted to a dictionary.
        - my_dict (dict): A dictionary to store the converted JSON object.

        Returns:
        - dict: A dictionary representation of the JSON object.
        """

        # A recursive function to iterate through the dictionary
        def iterate_dict(json_object, my_dict={}):

            try:
                for k, v in dict(json_object).items():
                    # if values are a list
                    if isinstance(v, list):

                        # if list has only one entry, e.g., key : []
                        if len(v) == 0:
                            if k not in my_dict:
                                my_dict[k] = {}

                        # if list contains only one key, e.g., key : ['brandinstances']
                        elif len(v) == 1:
                            if isinstance(v[0], dict):
                                my_dict[k] = {}
                                my_dict[k] = iterate_dict(v[0], my_dict[k])
                            else:
                                my_dict[k] = v

                        # if the list contains one nested list, e.g., key: [[]]
                        elif isinstance(v[0], list) and k not in my_dict and len(v[0]) == 1:
                            my_dict[k] = iterate_dict(v[0][0])

                        # if the nested object is a dictionary, e.g., key : [{}]
                        elif isinstance(v[0], dict) and k not in my_dict:
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v[0], my_dict[k])

                        # if the list contains multiple dictionaries [{},{},{}] or lists [[],[],[]]
                        else:
                            if k not in my_dict:
                                my_dict[k] = {}
                                for i in v:
                                    if isinstance(i, str):
                                        my_dict[k] = i
                                    elif isinstance(i, list) and len(i) == 1:
                                        my_dict[k] = iterate_dict(i[0], my_dict[k])
                                    elif isinstance(i,bool) or isinstance(i,int):
                                        my_dict[k] = i
                                    else:
                                        my_dict[k] = iterate_dict(i, my_dict[k])

                    else:
                        if k == "parameters" or k == "paths" or k == "actions" or k == "properties":
                            my_dict[k] = {}
                            for i in v:
                                if isinstance(i,dict):
                                    my_dict[k] = iterate_dict(v[str(i)], my_dict[k])
                                else:
                                    my_dict[k] = v[str(i)]
                        elif isinstance(v, dict):
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v,my_dict[k])
                        elif k not in my_dict:
                            my_dict[k] = v

            except Exception as ex:
                raise ex

            return my_dict
        return iterate_dict(json_object,my_dict)


    def map_values(self, my_dict) -> dict:
        """
        Load a JSON file and return a dictionary with mapped values.

        Args:
        - filename (str): Path to the JSON file.

        Returns:
        - dict: A dictionary with mapped values.
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as yaml_file:
                playbook_json = json.load(yaml_file)
                return self.get_dictionary(playbook_json, my_dict)

        except Exception as ex:
             raise ex

    def handle_conditions(self, dictionary, steps) -> dict:
        """Recursively handles the conditions in a dictionary and appends steps to a list.

        Args:
        - dictionary (dict): Dictionary to handle the conditions of.
        - steps (list): List to append the steps to.

        Returns:
        - list: Steps with the conditions handled.
        """

        for key, value in dictionary.items():
            if key == "actions":
                # If the current key is "actions", call handle_conditions with the corresponding value
                steps = self.handle_conditions(value, steps)
            elif "Condition" in key:
                # If the current key contains "Condition", append an If step to the steps list
                steps.append({"name": key, "type": "If", "actuator": ""})
                steps = self.handle_conditions(value["actions"], steps)
            elif key == "else":
                # If the current key is "else", call handle_conditions with the corresponding value
                steps = self.handle_conditions(value["actions"], steps)
            elif key == "runAfter":
                # If the current key is "runAfter", call handle_conditions with the corresponding value
                steps = self.handle_conditions(value, steps)
            elif isinstance(value, dict):
                # If the value is a dictionary, append a step to the steps list with the corresponding name, type and actuator
                actuator = self.get_actuator(value)
                step_type = value.get("type", "")
                steps.append({"name": key, "type": step_type, "actuator": actuator})
        return steps


    def get_actuator(self, key) -> str:
        """
        Extracts an actuator from a dictionary.

        Args:
        - key (dict): A dictionary containing the key-value pairs.

        Returns:
        - str: The actuator extracted from the dictionary.
        """
        actuator = ""
        # Check if the key contains the 'inputs' field
        if "inputs" in key:
            inputs = key["inputs"]  # store the 'inputs' field in a variable for convenience
            # Check if the 'inputs' field is a dictionary
            if isinstance(inputs, dict):
                # Check if the 'host' field is in the 'inputs' dictionary
                if "host" in inputs and "connection" in inputs["host"]:
                    # Extract the connection name from the 'host' field and store it in the 'actuator' variable
                    actuator = inputs["host"]["connection"]["name"].split("'")[3]
                # Check if the 'uri' field is in the 'inputs' dictionary
                elif "uri" in inputs:
                    # Store the URI in the 'actuator' variable
                    actuator = inputs["uri"]
                # Check if the 'connection' field is in the 'inputs' dictionary
                elif "connection" in inputs:
                    # Store the connection name in the 'actuator' variable
                    actuator = inputs["connection"]["name"]
                # Check if the 'content' field is in the 'inputs' dictionary
                elif "content" in inputs:
                    # Use regular expressions to extract the value in the parentheses and store it in the 'actuator' variable
                    actuator = re.findall(r'\(s.*?\)', str(inputs["content"]))
                    actuator = " ".join(actuator) if len(actuator) == 0 else actuator[0]
        return actuator

    def analyze_playbook(self, analysis_dict) -> dict:
        """
        Analyzes the JSON playbook and updates the provided dictionary with the extracted values.

        Args:
        - analysis_dict: A dictionary object to update with extracted values.

        Returns: 
        - A dictionary object.
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as yaml_file:
                playbook_json = json.load(yaml_file)
                # Extract steps
                if isinstance(playbook_json["resources"], dict):
                    steps = playbook_json["resources"]["properties"]["actions"]
                else:
                    steps = []
                    for action in playbook_json["resources"]:
                        if action["type"] == "Microsoft.Logic/workflows":
                            for key, value in action["properties"]["definition"]["actions"].items():
                                if key == "For_each":
                                    steps.append({"name": key, "type": "ForEach", "actuator": ""})
                                    steps = self.handle_conditions(value, steps)
                                else:
                                    actuator = self.get_actuator(value)
                                    steps.append({"name": key, "type": value["type"], "actuator": actuator})

                # Extract playbook metadata
                metadata = playbook_json.get("metadata", {})
                name = metadata.get("title", "") or metadata.get("parameters", {}).get("PlaybookName", {}).get("defaultValue", "")
                description = metadata.get("description", metadata.get("comment", "")).replace("\n", "")
                tags = metadata.get("tags", [])

                # Add actuator to analysis_dict
                if "actuator" not in analysis_dict:
                    analysis_dict["actuator"] = []
                actuator = [step["actuator"] for step in steps]
                analysis_dict["actuator"].append(actuator)

                # Add vendor to analysis_dict
                analysis_dict.setdefault("vendor", []).append("MS Azure")

                # Add tags to analysis_dict
                analysis_dict.setdefault("tags", []).append(tags)

                # Add number of steps to analysis_dict
                analysis_dict.setdefault("steps", []).append(len(steps))

                # Add step types to analysis_dict
                analysis_dict.setdefault("step_types", []).append([step["type"] for step in steps])

                # Add step names to analysis_dict
                analysis_dict.setdefault("step_names", []).append([step["name"].split("_")[0] for step in steps if "name" in step])

                # Add playbook name to analysis_dict
                analysis_dict.setdefault("playbook_name", []).append(name.strip())

                # Add playbook description to analysis_dict
                analysis_dict.setdefault("playbook_description", []).append(description)

                return analysis_dict

        except Exception as ex:
             raise ex
