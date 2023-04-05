"""
Module for transforming Rapid7 playbooks.
"""

import json


class Rapid7():
    """
    A playbook transformation class. Converts Rapid7-specific playbooks into a JSON schema.
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
        Recursively iterate through a dictionary and convert all lists to dictionaries where possible.

        Args:
        - json_object (dict): The dictionary object to be converted.
        - my_dict (dict): An optional dictionary object to update with the converted content.

        Returns:
        A dictionary object with all lists converted to dictionaries where possible.
        """

        try:
            for k, v in dict(json_object).items():

                # Check if the value is a list
                if isinstance(v, list):

                    # If the list is empty
                    if len(v) == 0:
                        if k not in my_dict:
                            my_dict[k] = {}

                    # If the list contains only one item
                    elif len(v) == 1:

                        # If the item is a dictionary
                        if isinstance(v[0], dict):
                            my_dict[k] = {}
                            my_dict[k] = self.get_dictionary(v[0], my_dict[k])

                        # If the item is not a dictionary
                        else:
                            my_dict[k] = v

                    # If the list contains one nested list
                    elif isinstance(v[0], list) and k not in my_dict and len(v[0]) == 1:
                        my_dict[k] = self.get_dictionary(v[0][0])

                    # If the nested object is a dictionary
                    elif isinstance(v[0], dict) and k not in my_dict:
                        my_dict[k] = {}
                        my_dict[k] = self.get_dictionary(v[0], my_dict[k])

                    # If the list contains multiple dictionaries or lists
                    else:
                        if k not in my_dict:
                            my_dict[k] = {}
                            for i in v:
                                if isinstance(i, (str, int, bool)):
                                    my_dict[k] = i
                                elif isinstance(i, list) and len(i) == 1:
                                    my_dict[k] = self.get_dictionary(
                                        i[0], my_dict[k])
                                else:
                                    my_dict[k] = self.get_dictionary(
                                        i, my_dict[k])

                # If the value is not a list
                else:
                    # If the key is one of the Rapid7-specific keys
                    if k in ["graphs", "steps", "edges", "nodes", "properties", "definitions"]:
                        my_dict[k] = {}
                        for i in v:
                            if isinstance(i, dict):
                                my_dict[k] = self.get_dictionary(i, my_dict[k])
                            else:
                                my_dict[k] = i

                    # If the value is a dictionary
                    elif isinstance(v, dict):
                        my_dict[k] = {}
                        my_dict[k] = self.get_dictionary(v, my_dict[k])

                    # If the value is not a dictionary
                    else:
                        my_dict[k] = v

        except:
            raise

        return my_dict

    def map_values(self, my_dict={}) -> dict:
        """
        Load a JSON file and return a dictionary with mapped values.

        Args:
        - filename (str): Path to the JSON file.

        Returns:
        - dict: A dictionary with mapped values.
        """
        try:
            # open the playbook file
            with open(self.filename, 'r', encoding='utf-8') as file:
                # load the JSON data from the file
                playbook_data = json.load(file)
                # call the get_dictionary method to transform the data into a dictionary
                return self.get_dictionary(playbook_data, my_dict)
        except:
            # if there's an error, raise an exception
            raise

    def analyze_playbook(self, analysis_dict) -> dict:
        """
        Analyzes the JSON playbook and updates the provided dictionary with the extracted values.

        Args:
        -  analysis_dict: A dictionary object to update with extracted values.

        Returns: 
        - A dictionary object.
        """

        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                # Load the JSON data from the file
                playbook_json = json.load(file)

                # Extract various information from the JSON data
                steps = [step for step in playbook_json["kom"]
                             ["workflowVersions"][0]["steps"].values()]
                tags = playbook_json["kom"]["workflowVersions"][0].get(
                    "tags", []) if playbook_json["kom"]["workflowVersions"][0]["tags"] is not None else []
                name = playbook_json["kom"]["workflowVersions"][0]["name"]
                description = playbook_json["kom"]["workflowVersions"][0]["description"]

                # Extract the playbook description from the description field of the JSON data
                if "# Description\n\n" in description:
                    description = description.split("\n\n")
                    description = description[1] if len(description) > 0 else ""
                elif "# Description\r\n\r\n" in description: 
                    description = description.split("\r\n\r\n")
                    description = description[1] if len(description) > 0 else ""
                elif "# Documentation\n\n## Setup\n\n" in description:
                    description = description.split("##")[1].replace("\n\n", " ")
                description = description.replace("\n", "").replace(";", "")

                # Add the extracted information to the analysis dictionary
                analysis_dict.setdefault("actuator", []).append(
                    [step.get("plugin", {}).get("name", "") if "plugin" in step else "" for step in steps])
                analysis_dict.setdefault("vendor", []).append("Rapid7")
                analysis_dict.setdefault("tags", []).append(tags)
                analysis_dict.setdefault("steps", []).append(len(steps))
                analysis_dict.setdefault("step_types", []).append(
                    [str(step["type"]) if "type" in step else "" for step in steps])
                analysis_dict.setdefault("step_names", []).append(
                    [str(step["name"]) if "name" in step else "" for step in steps])
                analysis_dict.setdefault("playbook_name", []).append(name)
                analysis_dict.setdefault(
                    "playbook_description", []).append(description)

                return analysis_dict
        except:
            raise
