"""
Module for transforming Catalyst playbooks.
"""

import json
from msilib.schema import Error
import yaml


class Catalyst():
    """
    A playbook transformation class. Converts Catalyst-specific playbooks into a JSON schema.
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
        Recursively converts a Catalyst-specific playbook into a JSON schema.

        Args:
            json_object (dict): The Catalyst-specific playbook to be converted.
            my_dict (dict): The resulting JSON schema. Used for recursion.

        Returns:
            dict: The resulting JSON schema.
        """

        # A recursive function to iterate through the dictionary
        def iterate_dict(json_object, my_dict={}) -> dict:
            try:
                for key, value in json_object.items():

                    if isinstance(value, list):
                        # if the value is a list

                        if len(value) == 0:
                            # if the list is empty
                            if key not in my_dict:
                                my_dict[key] = []
                        elif len(value) == 1:
                            # if the list has only one item
                            my_dict[key] = value
                        elif isinstance(value[0], list) and key not in my_dict and len(value[0]) == 1:
                            # if the list has one nested list
                            my_dict[key] = iterate_dict(value[0][0], {})
                        elif isinstance(value[0], dict) and key not in my_dict:
                            # if the list has one nested dictionary
                            my_dict[key] = {}
                            my_dict[key] = iterate_dict(value[0], my_dict[key])
                        else:
                            # if the list has multiple dictionaries or lists
                            if key not in my_dict:
                                my_dict[key] = {}
                                for item in value:
                                    if isinstance(item, str):
                                        my_dict[key] = item
                                    elif isinstance(item, list) and len(item) == 1:
                                        my_dict[key] = iterate_dict(
                                            item[0], my_dict[key])
                                    else:
                                        my_dict[key] = iterate_dict(
                                            item, my_dict[key])
                    else:
                        # if the value is not a list
                        if key == "tasks":
                            # if the key is 'tasks'
                            my_dict[key] = {}
                            for item in value:
                                my_dict[key] = iterate_dict(
                                    value[str(item)], my_dict[key])
                        elif isinstance(value, dict):
                            # if the value is a dictionary
                            my_dict[key] = {}
                            my_dict[key] = iterate_dict(value, my_dict[key])
                        elif key not in my_dict:
                            # if the key is not already in the dictionary
                            my_dict[key] = value
            except:
                print(f"{key} : {value}")

            return my_dict

        return iterate_dict(json_object, my_dict)


    def map_values(self, my_dict={}) -> dict:
        """
        Load a YAML file and return a dictionary with mapped values.

        Args:
        - filename (str): Path to the YAML file.

        Returns:
        - dict: A dictionary with mapped values.
        """

        # Open the file specified in the `filename` attribute and load its contents as a YAML object
        with open(self.filename, 'r', encoding='utf-8') as file:
            playbook_yml = yaml.safe_load(file)

        # Convert the YAML object to a JSON string with indentation and custom string conversion function
        playbook_json = json.dumps(playbook_yml, indent=4, default=str)

        # Convert the JSON string to a Python object
        playbook_object = json.loads(playbook_json)

        # Call the `get_dictionary` method to map the values of the object to the specified dictionary
        return self.get_dictionary(playbook_object, my_dict)


    def analyze_playbook(self, analysis_dict) -> dict:
        """
        Analyzes the YAML playbook and updates the provided dictionary with the extracted values.

        Args:
        - analysis_dict: A dictionary object to update with extracted values.

        Returns: 
        - A dictionary object.
        """

        try:
            # Open and read the playbook YAML file
            with open(self.filename, 'r', encoding='utf-8') as file:
                playbook_yml = yaml.safe_load(file)

            # Convert YAML to JSON and parse the JSON object
            playbook_json = json.dumps(playbook_yml, indent=4, default=str)
            playbook_object = json.loads(playbook_json)

            # Extract playbook information
            name = playbook_object["name"]
            steps = list(playbook_object["tasks"].values())

            # Add vendor information to analysis dictionary
            analysis_dict.setdefault("vendor", []).append("Catalyst")

            # Extract tags information and add to analysis dictionary
            tags = playbook_object.get("tags", [])
            analysis_dict.setdefault("tags", []).append(tags)

            # Extract actuator information and add to analysis dictionary
            actuator = [step.get("automation", "") for step in steps]
            analysis_dict.setdefault("actuator", []).append(actuator)

            # Extract number of steps and add to analysis dictionary
            num_steps = len(steps)
            analysis_dict.setdefault("steps", []).append(num_steps)

            # Extract step types and add to analysis dictionary
            step_types = [step.get("type", "") for step in steps]
            analysis_dict.setdefault("step_types", []).append(step_types)

            # Extract step names and add to analysis dictionary
            step_names = [step.get("name", "") for step in steps]
            analysis_dict.setdefault("step_names", []).append(step_names)

            # Add playbook name and description to analysis dictionary
            analysis_dict.setdefault("playbook_name", []).append(name)
            analysis_dict.setdefault("playbook_description", []).append("")

            return analysis_dict

        except:
            raise
