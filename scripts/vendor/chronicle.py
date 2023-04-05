import json


class Chronicle:
    """
    A playbook transformation class. Converts Siemplify-specific playbooks into a JSON schema.
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

        for k, v in json_object.items():
            # if values are a list
            if isinstance(v, list):
                # if list has only one entry, e.g., key : []
                if len(v) == 0:
                    if k not in my_dict:
                        my_dict[k] = []

                # if list contains only one key, e.g., key : ['brandinstances']
                elif len(v) == 1:
                    my_dict[k] = v

                # if the list contains one nested list, e.g., key: [[]]
                elif isinstance(v[0], list) and k not in my_dict and len(v[0]) == 1:
                    my_dict[k] = self.get_dictionary(v[0][0])

                # if the nested object is a dictionary, e.g., key : [{}]
                elif isinstance(v[0], dict) and k not in my_dict:
                    my_dict[k] = {}
                    my_dict[k] = self.get_dictionary(v[0], my_dict[k])

                # if the list contains multiple dictionaries [{},{},{}] or lists [[],[],[]]
                else:
                    if k not in my_dict:
                        my_dict[k] = {}
                        for i in v:
                            if isinstance(i, str):
                                my_dict[k] = i
                            elif isinstance(i, list) and len(i) == 1:
                                my_dict[k] = self.get_dictionary(
                                    i[0], my_dict[k])
                            else:
                                my_dict[k] = self.get_dictionary(i, my_dict[k])

            else:
                if isinstance(v, dict):
                    my_dict[k] = {}
                    my_dict[k] = self.get_dictionary(v, my_dict[k])
                elif k not in my_dict:
                    my_dict[k] = v

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
            with open(self.filename, 'r', encoding='utf-8') as file:
                playbook_json = json.load(file)
                return self.get_dictionary(playbook_json, my_dict)
        except:
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
            # Load the playbook file as JSON
            with open(self.filename, 'r', encoding='utf-8') as file:
                playbook_json = json.load(file)

            # Extract details from the playbook
            steps = playbook_json["steps"]
            name = playbook_json["name"]
            description = playbook_json.get(
                "description", "").replace("\n", " ")

            # Update analysis_dict with actuator details
            actuator = [step.get("integration", "") for step in steps]
            analysis_dict.setdefault("actuator", []).append(actuator)

            # Add vendor information to analysis_dict
            analysis_dict.setdefault("vendor", []).append("Chronicle")

            # Add tags information to analysis_dict
            tags = []  # Empty list, not sure why the original code had a loop here
            analysis_dict.setdefault("tags", []).append(tags)

            # Add number of steps to analysis_dict
            analysis_dict.setdefault("steps", []).append(len(steps))

            # Add step types to analysis_dict
            step_types = [str(step["type"]) if "type" in step else "" for step in steps]
            analysis_dict.setdefault("step_types", []).append(step_types)

            # Add step names to analysis_dict
            step_names = [str(step["name"].split("_")[1]) if len(step["name"].split("_")) > 1 else step["name"] for step in steps]
            analysis_dict.setdefault("step_names", []).append(step_names)

            # Add playbook name to analysis_dict
            analysis_dict.setdefault("playbook_name", []).append(name)

            # Add playbook description to analysis_dict
            analysis_dict.setdefault(
                "playbook_description", []).append(description)

            return analysis_dict

        except:
            # Raise an exception if an error occurs
            raise
