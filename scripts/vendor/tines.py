import json


class Tines:
    """
    A playbook transformation class. Converts Tines-specific playbooks into a JSON schema.
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
        Recursively converts a ThreatConnect-specific playbook into a JSON schema.

        Args:
            json_object (dict): The ThreatConnect-specific playbook to be converted.
            my_dict (dict): The resulting JSON schema. Used for recursion.

        Returns:
            dict: The resulting JSON schema.
        """

        # A recursive function to iterate through the dictionary
        def iterate_dict(json_object, my_dict={}) -> dict:

            try:
                for k, v in dict(json_object).items():
                    # if the value is a list
                    if isinstance(v, list):
                        # if the list has only one entry, e.g., key: []
                        if len(v) == 0:
                            # create an empty dictionary for the key if it doesn't exist
                            if k not in my_dict:
                                my_dict[k] = {}
                        # if the list contains only one key, e.g., key: ['brandinstances']
                        elif len(v) == 1:
                            if isinstance(v[0], dict):
                                # create an empty dictionary for the key and call the function recursively
                                my_dict[k] = {}
                                my_dict[k] = iterate_dict(v[0], my_dict[k])
                            else:
                                # set the value of the key to the single value in the list
                                my_dict[k] = v
                        # if the list contains one nested list, e.g., key: [[]]
                        elif isinstance(v[0], list) and k not in my_dict and len(v[0]) == 1:
                            # call the function recursively with the nested list as input
                            my_dict[k] = iterate_dict(v[0][0])
                        # if the nested object is a dictionary, e.g., key: [{}]
                        elif isinstance(v[0], dict) and k not in my_dict:
                            # create an empty dictionary for the key and call the function recursively
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v[0], my_dict[k])
                        # if the list contains multiple dictionaries [{},{},{}] or lists [[],[],[]]
                        else:
                            if k not in my_dict:
                                my_dict[k] = {}
                                for i in v:
                                    if isinstance(i, str) or isinstance(i, int) or isinstance(i, bool):
                                        # set the value of the key to the primitive type
                                        my_dict[k] = i
                                    elif isinstance(i, list) and len(i) == 1:
                                        # call the function recursively with the nested list as input
                                        my_dict[k] = iterate_dict(
                                            i[0], my_dict[k])
                                    else:
                                        # call the function recursively with the dictionary or list as input
                                        my_dict[k] = iterate_dict(
                                            i, my_dict[k])
                    else:
                        # For certain keys, create a nested dictionary and populate it with the appropriate key-value pairs
                        if k == "items" or k == "fields" or k == "out":
                            my_dict[k] = {}
                            for i in v:
                                if isinstance(i, dict):
                                    my_dict[k] = iterate_dict(i, my_dict[k])
                                else:
                                    # set the value of the key to the single value
                                    my_dict[k] = i
                        elif isinstance(v, dict):
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v, my_dict[k])
                        else:
                            # For certain keys, the value is an empty string, e.g., key: "description"
                            if k == "description" or k == "content" or k == "diagram_layout":
                                v = ""
                            my_dict[k] = v
            except:
                # If there is an error, print the key-value pair that caused the error
                print(f"{k} : {v}")

            return my_dict
        # Call the iterate_dict function
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
            # Open the playbook file in read mode
            with open(self.filename, 'r', encoding='utf-8') as file:
                # Load the playbook file into a JSON object
                playbook_json = json.load(file)
                # Call the get_dictionary method to extract information from the playbook and return it as a dictionary
                return self.get_dictionary(playbook_json, my_dict)
        except:
            # Raise an exception if there was an error reading or processing the playbook file
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
            # Read the playbook file
            with open(self.filename, 'r', encoding='utf-8') as file:
                playbook_json = json.load(file)

                # Add vendor information to analysis_dict
                analysis_dict.setdefault('vendor', []).append('Tines')

                # Extract tags from playbook description and add to analysis_dict
                tags = []
                descriptions = playbook_json.get('description', '').split('\n')
                for description in descriptions:
                    if 'tags' in description:
                        desc_tags = description.replace(
                            'tags: ', '').split(',')
                        for tag in desc_tags:
                            if tag:
                                tags.append(tag.strip())
                analysis_dict.setdefault('tags', []).append(tags)

                # Extract actuator information from playbook tasks and add to analysis_dict
                actuator = []
                for task in playbook_json.get('agents', []):
                    mode = task.get('options', {}).get('mode', '')
                    if mode in ['post', 'put', 'get']:
                        actuator.append(task['options']['url'])
                    elif mode == 'explode':
                        actuator.append(task['options']['path'])
                    elif mode == 'implode':
                        actuator.append(task['options'].get('guid_path', ''))
                    else:
                        actuator.append('')
                analysis_dict.setdefault('actuator', []).append(actuator)

                # Extract step information from playbook tasks and add to analysis_dict
                steps = len(playbook_json.get('agents', []))
                analysis_dict.setdefault('steps', []).append(steps)

                # Extract step type information from playbook tasks and add to analysis_dict
                step_types = [step.get('type', '') if "type" in step else ""
                              for step in playbook_json.get('agents', [])]
                analysis_dict.setdefault('step_types', []).append(step_types)

                # Extract step name information from playbook tasks and add to analysis_dict
                step_names = [str(step.get('name', '')) if "name" in step else ""
                              for step in playbook_json.get('agents', [])]
                analysis_dict.setdefault('step_names', []).append(step_names)

                # Extract playbook name and description and add to analysis_dict
                analysis_dict.setdefault('playbook_name', []).append(
                    str(playbook_json.get('name', '')))
                analysis_dict.setdefault('playbook_description', []).append(
                    playbook_json.get('description', '').split('\n')[0])

                return analysis_dict
        except:
            raise
