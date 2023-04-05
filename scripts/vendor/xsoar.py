import json
import yaml


class Xsoar:
    """
    A playbook transformation class. Converts XSOAR-specific playbooks into a JSON schema.
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
                if isinstance(v, list):
                    if len(v) == 0:
                        if k not in my_dict:
                            my_dict[k] = []
                    elif len(v) == 1:
                        my_dict[k] = {}
                        my_dict[k] = self.get_dict(v[0], my_dict[k])
                    elif isinstance(v[0], list) and k not in my_dict and len(v[0]) == 1:
                        my_dict[k] = self.get_dict(v[0][0])
                    elif isinstance(v[0], dict) and k not in my_dict:
                        my_dict[k] = {}
                        my_dict[k] = self.get_dict(v[0], my_dict[k])
                    else:
                        if k not in my_dict:
                            my_dict[k] = {}
                            for i in v:
                                if isinstance(i, str):
                                    my_dict[k] = i
                                elif isinstance(i, list) and len(i) == 1:
                                    my_dict[k] = self.get_dict(
                                        i[0], my_dict[k])
                                else:
                                    my_dict[k] = self.get_dict(i, my_dict[k])
                else:
                    if k == "tasks":
                        my_dict[k] = {}
                        for i in v:
                            my_dict[k] = self.get_dict(v[str(i)], my_dict[k])
                    elif isinstance(v, dict):
                        my_dict[k] = {}
                        my_dict[k] = self.get_dict(v, my_dict[k])
                    elif k not in my_dict:
                        my_dict[k] = v
        except:
            pass
        return my_dict

    def map_values(self, my_dict={}) -> dict:
        """
        Load a YAML file and return a dictionary with mapped values.

        Args:
        - filename (str): Path to the YAML file.

        Returns:
        - dict: A dictionary with mapped values.
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                playbook_yml = yaml.safe_load(file)
        except:
            with open(self.filename, 'r', encoding='utf-8') as file:
                yaml_string = file.read().replace('simple: =', 'simple: "="')
                playbook_yml = yaml.safe_load(yaml_string)

        playbook_json = json.dumps(playbook_yml, indent=4, default=str)
        try:
            playbook_object = json.loads(playbook_json)
        except:
            raise ValueError("Error parsing playbook JSON.")

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
            # Open the playbook file and load its contents as YAML
            with open(self.filename, 'r', encoding='utf-8') as file:
                playbook_yml = yaml.safe_load(file)
                # Convert the YAML to JSON for easier manipulation
                playbook_json = json.dumps(playbook_yml, indent=4, default=str)
                playbook_json = json.loads(playbook_json)

            # Extract playbook metadata
            name = playbook_json["name"]
            description = playbook_json["description"].replace(
                "\n", " ").replace(";", "")

            # Extract playbook steps
            steps = playbook_json["tasks"].values()

            # Add vendor to analysis dict
            analysis_dict.setdefault("vendor", []).append("XSOAR")

            # Extract actuator information and add to analysis dict
            actuator_brands = [step["task"].get("brand", "") for step in steps]
            analysis_dict.setdefault("actuator", []).append(actuator_brands)

            # Extract tags and add to analysis dict
            tags = playbook_json.get("tags", [])
            analysis_dict.setdefault("tags", []).append(tags)

            # Add number of steps to analysis dict
            analysis_dict.setdefault("steps", []).append(len(steps))

            # Extract step types and add to analysis dict
            step_types = [step["type"] if "type" in step else "" for step in steps]
            analysis_dict.setdefault("step_types", []).append(step_types)

            # Extract step names and add to analysis dict
            step_names = [step["task"]["name"] if "task" in step else "" for step in steps]
            analysis_dict.setdefault("step_names", []).append(step_names)

            # Add playbook name and description to analysis dict
            analysis_dict.setdefault("playbook_name", []).append(name)
            analysis_dict.setdefault(
                "playbook_description", []).append(description)

            # Return the updated analysis dict
            return analysis_dict

        except:
            # Raise an error if there was a problem reading the playbook
            raise
