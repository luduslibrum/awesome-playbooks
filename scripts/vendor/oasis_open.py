import json


class OasisOpen:
    """
    Oasis Open playbook transformation class.
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
        def iterate_dict(json_object, my_dict={}) -> dict:

            try:
                for k, v in dict(json_object).items():
                    # if values are a list
                    if isinstance(v, list):
                        # if list has only one entry, e.g., key : []
                        if len(v) == 0:
                            if k not in my_dict:
                                my_dict[k] = []
                        # if list contains only one key, e.g., key : ['brandinstances']
                        elif len(v) == 1:
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v[0], my_dict[k])
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
                                        my_dict[k] = iterate_dict(
                                            i[0], my_dict[k])
                                    else:
                                        my_dict[k] = iterate_dict(
                                            i, my_dict[k])
                    else:
                        # If the key is 'workflow', iterate through its values.
                        if k == "workflow":
                            my_dict[k] = {}
                            for i in v:
                                my_dict[k] = iterate_dict(
                                    v[str(i)], my_dict[k])
                        # If the value is a dictionary, convert it to a dictionary.
                        elif isinstance(v, dict):
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v, my_dict[k])
                        # If the key is not in the dictionary, add it to the dictionary.
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
            # Open and read the JSON file
            with open(self.filename, 'r', encoding='utf-8') as file:
                json_object = json.load(file)

                # Call the 'get_dictionary' function to map the values of the JSON object
                return self.get_dictionary(json_object, my_dict)

        except:
            # Raise an exception if an error occurs
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
            with open(self.filename, 'r', encoding='utf-8') as file:
                playbook_json = json.load(file)

                # Extract workflow steps from playbook JSON
                steps = list(playbook_json["workflow"].values())

                # Extract playbook metadata
                name = playbook_json["name"]
                description = playbook_json["description"]
                tags = playbook_json["labels"]

                # Extract actuator commands from workflow steps
                actuator = [step["commands"][0]["command"]
                            if "commands" in step else "" for step in steps]

                # Add extracted data to analysis_dict
                analysis_dict.setdefault("actuator", []).append(actuator)
                analysis_dict.setdefault("vendor", []).append("OasisOpen")
                analysis_dict.setdefault("tags", []).append(tags)
                analysis_dict.setdefault("steps", []).append(len(steps))
                analysis_dict.setdefault("step_types", []).append(
                    [step["type"] if "type" in step else "" for step in steps])
                analysis_dict.setdefault("step_names", []).append(
                    [str(step["name"]) if "name" in step else "" for step in steps])
                analysis_dict.setdefault("playbook_name", []).append(name)
                analysis_dict.setdefault(
                    "playbook_description", []).append(description)

                return analysis_dict

        except:
            raise
