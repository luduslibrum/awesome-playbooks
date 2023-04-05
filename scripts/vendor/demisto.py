import json
from msilib.schema import Error
import yaml
import re

class Demisto():
    """
    A playbook transformation class. Converts Demisto-specific playbooks into a JSON schema.
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
        Recursively converts a Demisto-specific playbook into a JSON schema.

        Args:
            json_object (dict): The Demisto-specific playbook to be converted.
            my_dict (dict): The resulting JSON schema. Used for recursion.

        Returns:
            dict: The resulting JSON schema.
        """

        # A recursive function to iterate through the dictionary
        def iterate_dict(json_object, my_dict):
            for k, v in json_object.items():

                # If the value is a list
                if isinstance(v, list):

                    # If the list is empty
                    if len(v) == 0:
                        if k not in my_dict:
                            my_dict[k] = []

                    # If the list has only one item
                    elif len(v) == 1:
                        my_dict[k] = v[0]

                    # If the list contains only one nested list
                    elif isinstance(v[0], list) and len(v[0]) == 1:
                        my_dict[k] = iterate_dict(v[0][0], {})

                    # If the list contains one or more dictionaries or lists
                    else:
                        my_dict[k] = []
                        for i in v:
                            if isinstance(i, str):
                                my_dict[k].append(i)
                            elif isinstance(i, list) and len(i) == 1:
                                my_dict[k].append(iterate_dict(i[0], {}))
                            else:
                                my_dict[k].append(iterate_dict(i, {}))

                # If the value is a dictionary
                elif isinstance(v, dict):

                    # Here is the main difference for each vendor
                    if k == "tasks":
                        my_dict[k] = {}
                        for i in v:
                            my_dict[k][i] = iterate_dict(v[i], {})
                    else:
                        my_dict[k] = iterate_dict(v, {})

                # If the value is neither a list nor a dictionary
                else:
                    my_dict[k] = v

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
        
        # Open and read a YAML file.
        with open(self.filename, 'r', encoding='utf-8') as file:
            # Parse the YAML data into a Python data structure.
            playbook_yml = yaml.safe_load(file)

        # Convert the Python data structure to a JSON string.
        playbook_json = json.dumps(playbook_yml, indent=4, default=str)

        # Parse the JSON string into a Python dictionary.
        try:
            playbook_object = json.loads(playbook_json)
        except Error:
            # Raise an error if the JSON parsing fails.
            raise Error

        # Call the get_dictionary method to create a nested dictionary from the parsed JSON object.
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
            # open the YAML file and load it as a Python dictionary
            with open(self.filename, 'r', encoding='utf-8') as file:
                playbook_yml = yaml.safe_load(file)

            # convert the Python dictionary to a JSON object
            playbook_json = json.dumps(playbook_yml, indent=4, default=str)
            playbook_json = json.loads(playbook_json)

            # extract the tasks from the playbook JSON object
            tasks = playbook_json.get("tasks", {})
            tasks = list(tasks.values())

            # update the tasks in the playbook JSON object
            playbook_json["tasks"] = tasks

            # update the vendor information in the analysis dictionary
            analysis_dict.setdefault("vendor", []).append("Demisto")

            # extract the tags from the tasks and update the analysis dictionary
            tags = []
            for task in tasks:
                if "tags" in task:
                    tags.extend(task["tags"])
            analysis_dict.setdefault("tags", []).append(tags)

            # update the number of steps in the analysis dictionary
            analysis_dict.setdefault("steps", []).append(len(tasks))

            # extract the actuator information from the tasks and update the analysis dictionary
            actuator = [task["task"].get("brand", "") for task in tasks]
            analysis_dict.setdefault("actuator", []).append(actuator)

            # extract the step types from the tasks and update the analysis dictionary
            step_types = [task["type"] for task in tasks]
            analysis_dict.setdefault("step_types", []).append(step_types)

            # extract the step names from the tasks and update the analysis dictionary
            step_names = [] 
            for task in tasks:
                name = task["task"].get("name", "")
                name = " ".join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', name)).split())
                name = name.replace("-", " ")
                step_names.append(name)
            analysis_dict.setdefault("step_names", []).append(step_names)

            # update the playbook name in the analysis dictionary
            analysis_dict.setdefault("playbook_name", []).append(playbook_json.get("name", ""))

            # update the playbook description in the analysis dictionary
            description = playbook_json.get("description", "").replace("\n", "")
            analysis_dict.setdefault("playbook_description", []).append(description)

            return analysis_dict

        except Exception as e:
            raise e

