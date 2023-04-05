import json


class Fortinet():
    """
    A playbook transformation class. Converts Fortinet-specific playbooks into a JSON schema.
    """

    fortinet_step_types = {
        "/api/3/workflow_step_types/b348f017-9a94-471f-87f8-ce88b6a7ad62": "Start",
        "/api/3/workflow_step_types/04d0cf46-b6a8-42c4-8683-60a7eaa69e8f": "Configuration",
        "/api/3/workflow_step_types/12254cf5-5db7-4b1a-8cb1-3af081924b28": "Condition",
        "/api/3/workflow_step_types/74932bdc-b8b6-4d24-88c4-1a4dfbc524f3": "Playbook execution",
        "/api/3/workflow_step_types/0109f35d-090b-4a2b-bd8a-94cbc3508562": "Connector",
        "/api/3/workflow_step_types/2597053c-e718-44b4-8394-4d40fe26d357": "Manual task",
        "/api/3/workflow_step_types/fc04082a-d7dc-4299-96fb-6837b1baa0fe": "User decision",
        "/api/3/workflow_step_types/dc6ac63d-c5a5-472f-9eb4-6b18473a98b8": "User input",
        "/api/3/workflow_step_types/b593663d-7d13-40ce-a3a3-96dece928722": "API call",
        "/api/3/workflow_step_types/f414d039-bb0d-4e59-9c39-a8f1e880b18a": "Start",
        "/api/3/workflow_step_types/0bfed618-0316-11e7-93ae-92361f002671": "Connector",
        "/api/3/workflow_step_types/b593663d-7d13-40ce-a3a3-96dece928770": "Query/filter task",
        "/api/3/workflow_step_types/9300bf69-5063-486d-b3a6-47eb9da24872": "Start",
        "/api/3/workflow_step_types/ea155646-3821-4542-9702-b246da430a8d": "Start",
        "/api/3/workflow_step_types/ee73e569-2188-43fe-a7f0-1964ba82a4de": "Script",
        "/api/3/workflow_step_types/4c0019b2-055c-44d0-968c-678a0c2d762e": "Messaging",
        "/api/3/workflow_step_types/df26c7a2-4166-4ca5-91e5-548e24c01b5f": "Start",
        "/api/3/workflow_step_types/6832e556-b9c7-497a-babe-feda3bd27dcg": "Playbook execution",
        "/api/3/workflow_step_types/1fdd14cc-d6b4-4335-a3af-ab49c8ed2fd8": "Script",
        "/api/3/workflow_step_types/6832e556-b9c7-497a-babe-feda3bd27dbf": "Await"
    }


    def __init__(self, filename: str):
        """
        Initializes the class with the given filename.

        Args:
        - filename (str): The name of the file to be processed.
        """
        self.filename = filename


    def get_dictionary(self, json_object, my_dict={}) -> dict:
        """
        Recursively converts a Fortinet-specific playbook into a JSON schema.

        Args:
            json_object (dict): The Fortinet-specific playbook to be converted.
            my_dict (dict): The resulting JSON schema. Used for recursion.

        Returns:
            dict: The resulting JSON schema.
        """

        # A recursive function to iterate through the dictionary
        def iterate_dict(json_object, my_dict={}) -> dict:
            try:
                # iterate over the key-value pairs of the JSON object dictionary
                for k, v in dict(json_object).items():
                    # check if the value is a list
                    if isinstance(v, list):
                        # if the list is empty, create an empty list for the corresponding key
                        if len(v) == 0:
                            if k not in my_dict:
                                my_dict[k] = []
                        # if the list has only one element, recursively iterate over it and store the result in a new dictionary with the same key
                        elif len(v) == 1:
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v[0], my_dict[k])
                        # if the list contains a single nested list, recursively iterate over it and store the result in the same dictionary
                        elif isinstance(v[0], list) and k not in my_dict and len(v[0]) == 1:
                            my_dict[k] = iterate_dict(v[0][0])
                        # if the list contains a single nested dictionary, recursively iterate over it and store the result in a new dictionary with the same key
                        elif isinstance(v[0], dict) and k not in my_dict:
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v[0], my_dict[k])
                        # if the list contains multiple dictionaries or lists, iterate over each element of the list and store the results in a new dictionary with the same key
                        else:
                            if k not in my_dict:
                                my_dict[k] = {}
                                for i in v:
                                    # if the element is a string, store it as a value with the same key
                                    if isinstance(i, str): 
                                        my_dict[k] = i
                                    # if the element is a list with a single nested dictionary, recursively iterate over it and store the result in a new dictionary with the same key
                                    elif isinstance(i, list) and len(i) == 1:
                                        my_dict[k] = iterate_dict(i[0], my_dict[k])
                                    # if the element is a dictionary, recursively iterate over it and store the result in a new dictionary with the same key
                                    else:
                                        my_dict[k] = iterate_dict(i, my_dict[k])
                    # if the value is not a list, check if it is a dictionary
                    else:
                        if isinstance(v, dict):
                            # if the value is a dictionary, recursively iterate over it and store the result in a new dictionary with the same key
                            my_dict[k] = iterate_dict(v, my_dict[k])
                        # if the value is not a dictionary, store it as a value with the same key
                        elif k not in my_dict:
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
            with open(self.filename, 'r', encoding='utf-8') as file:
                playbook_json = json.load(file)
                return self.get_dictionary(playbook_json, my_dict)
        except:
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
            # Load the JSON playbook file
            with open(self.filename, 'r', encoding='utf-8') as file:
                playbook = json.load(file)

                # Extract and format the playbook description
                description = ""
                if "description" in playbook and playbook["description"] is not None:
                    description = playbook["description"].replace(
                        "\n", "").replace(";", "")

                # Extract and update the vendor information
                analysis_dict.setdefault("vendor", []).append("FortiSOAR")

                # Extract and update the tags information
                tags = playbook.get("recordTags", [])
                analysis_dict.setdefault("tags", []).append(tags)

                # Extract and update the actuator information
                actuator = [step["arguments"].get(
                    "connector", "") if "arguments" in step and "connector" in step["arguments"] else "" for step in playbook.get("steps", [])]
                analysis_dict.setdefault("actuator", []).append(actuator)

                # Extract and update the number of steps information
                analysis_dict.setdefault("steps", []).append(
                    len(playbook.get("steps", [])))

                # Extract and update the step types information
                step_types = [self.fortinet_step_types[step.get("stepType", "")]
                              for step in playbook.get("steps", [])]
                analysis_dict.setdefault("step_types", []).append(step_types)

                # Extract and update the step names information
                step_names = [step.get("name", "")
                              for step in playbook.get("steps", [])]
                analysis_dict.setdefault("step_names", []).append(step_names)

                # Extract and update the playbook name information
                analysis_dict.setdefault("playbook_name", []).append(
                    playbook.get("name", ""))

                # Extract and update the playbook description information
                analysis_dict.setdefault(
                    "playbook_description", []).append(description)

                # Return the updated analysis dictionary
                return analysis_dict

        except Exception as e:
            # Handle any exception by re-raising it
            raise e
