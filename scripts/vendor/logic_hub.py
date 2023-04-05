import json
import re

class LogicHub():
    """
    A playbook transformation class. Converts LogicHub-specific playbooks into a JSON schema.
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
        Recursively converts a LogicHub-specific playbook into a JSON schema.

        Args:
            json_object (dict): The LogicHub-specific playbook to be converted.
            my_dict (dict): The resulting JSON schema. Used for recursion.

        Returns:
            dict: The resulting JSON schema.
        """

        # A recursive function to iterate through the dictionary
        def iterate_dict(json_object, my_dict={}) -> dict:

            try:
                for k, v in json_object.items():
                    # Check if the value is a list
                    if isinstance(v, list):
                        # If the list is empty, create an empty list for the key
                        if len(v) == 0:
                            if k not in my_dict:
                                my_dict[k] = []
                        # If the list contains only one item, recursively create a dictionary for that item
                        elif len(v) == 1:
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v[0], my_dict[k])
                        # If the list contains one nested list, recursively create a dictionary for that nested list
                        elif isinstance(v[0], list) and k not in my_dict and len(v[0]) == 1:
                            my_dict[k] = iterate_dict(v[0][0])
                        # If the list contains one nested dictionary, recursively create a dictionary for that nested dictionary
                        elif isinstance(v[0], dict) and k not in my_dict:
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v[0], my_dict[k])
                        # If the list contains multiple dictionaries or lists, recursively create a dictionary for each item in the list
                        else:
                            if k not in my_dict:
                                my_dict[k] = {}
                            for i in v:
                                if isinstance(i, str):
                                    my_dict[k] = i
                                elif isinstance(i, list) and len(i) == 1:
                                    my_dict[k] = iterate_dict(i[0], my_dict[k])
                                else:
                                    my_dict[k] = iterate_dict(i, my_dict[k])
                    else:
                        # If the value is a dictionary, recursively create a dictionary for that dictionary
                        if isinstance(v, dict):
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v, my_dict[k])
                        else:
                            # If the key is one of a list of known keys, set the value to an empty string
                            if k in ["query", "keyColumns", "lql", "templateLQL", "description", "errorMessage"]:
                                v = ""
                            my_dict[k] = v
            except:
                pass
            return my_dict

        return iterate_dict(json_object, my_dict)

    def map_values(self, my_dict={}) -> dict:
        """
        Load a JSON file and return a dictionary with mapped values.

        Args:
        - filename (str): Path to the JSON file.

        Returns:
        - dict: A dictionary with mapped values.
        """

        try:
            # Open the specified file in read mode and load the content as JSON.
            with open(self.filename, 'r', encoding='utf-8') as file:
                playbook_json = json.load(file)

                # Call the get_dictionary method with the loaded JSON and the provided dictionary.
                modified_dict = self.get_dictionary(playbook_json, my_dict)

                # Return the modified dictionary.
                return modified_dict
        except:
            # Raise an exception if an error occurs while loading the JSON content.
            raise

    def analyze_playbook(self, analysis_dict) -> dict:
        """
        Analyzes the JSON playbook and updates the provided dictionary with the extracted values.

        Args:
        - analysis_dict: A dictionary object to update with extracted values.

        Returns: 
        - A dictionary object.
        """

        try:
            # Open the YAML playbook file and load its content as JSON
            with open(self.filename, 'r', encoding='utf-8') as file:
                playbook_json = json.load(file)

                # Get the steps from the first flow in the playbook
                steps = playbook_json["flows"][0]["nodes"]
                step_names = []
                actuators = []

                # For each step, extract its name and actuator
                for step in steps:
                    step_name = ""
                    step_actuator = ""

                    if "contentMetadata" in step:
                        # If the step has content metadata, use its name and action name
                        if "integrationId" in step["contentMetadata"]:
                            step_actuator = step["contentMetadata"]["name"]
                            step_name = step["contentMetadata"]["actionName"]
                    elif "integration" in step:
                        # If the step has an integration, use its integration ID and action ID
                        step_actuator = step["integration"]["integrationId"]
                        step_name = step["integration"]["actionId"]

                    # If no step name was found, use the step's name attribute
                    if step_name == "":
                        step_name = step["name"]

                    # Append the step's name and actuator to their respective lists
                    step_names.append(step_name)
                    actuators.append(step_actuator)
                
                # Preprocess step names
                for idx in range(len(step_names)):
                    step_names[idx] = " ".join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', step_names[idx] )).split())
                    step_names[idx]  = step_names[idx] .replace("_", " ")

                # Get the playbook's name, description, and tags
                name = playbook_json["flows"][0]["name"]
                description = ""
                tags = []

                if "tags" in playbook_json["modules"]:
                    for tag in playbook_json["modules"]["tags"]:
                        tags.append(tag)

                # Append analysis data to the analysis dictionary
                analysis_dict.setdefault("vendor", []).append("LogicHub")
                analysis_dict.setdefault("tags", []).append(tags)
                analysis_dict.setdefault("actuator", []).append(actuators)
                analysis_dict.setdefault("steps", []).append(len(steps))
                analysis_dict.setdefault("step_types", []).append(
                    [str(step["kind"]) if "kind" in steps else "" for step in steps])
                analysis_dict.setdefault("step_names", []).append(step_names)
                analysis_dict.setdefault("playbook_name", []).append(name)
                analysis_dict.setdefault(
                    "playbook_description", []).append(description)

                return analysis_dict

        except:
            raise
