import json
import os


class Splunk():
    """
    A playbook transformation class. Converts Splunk-specific playbooks into a JSON schema.
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
        Recursively converts a Splunk-specific playbook into a JSON schema.

        Args:
        - json_object (dict): The Splunk-specific playbook to be converted.
        - my_dict (dict): The resulting JSON schema. Used for recursion.

        Returns:
        - dict: The resulting JSON schema.
        """
   
        # A recursive function to iterate through the dictionary
        def iterate_dict(json_object, my_dict={}) -> dict:

            try:
                for k, v in dict(json_object).items():

                    # Handle lists
                    if isinstance(v, list):

                        # Handle empty lists
                        if len(v) == 0:
                            if k not in my_dict:
                                my_dict[k] = {}

                        # Handle lists with only one item
                        elif len(v) == 1:
                            if isinstance(v[0], dict):
                                my_dict[k] = {}
                                my_dict[k] = iterate_dict(v[0], my_dict[k])
                            else:
                                my_dict[k] = v

                        # Handle nested lists with only one item
                        elif isinstance(v[0], list) and k not in my_dict and len(v[0]) == 1:
                            my_dict[k] = iterate_dict(v[0][0])

                        # Handle nested lists with multiple items
                        elif isinstance(v[0], dict) and k not in my_dict:
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v[0], my_dict[k])
                        else:
                            my_dict[k] = {}
                            for i in v:
                                # Handle strings, integers, and booleans
                                if isinstance(i, str) or isinstance(i, int) or isinstance(i, bool):
                                    my_dict[k] = i
                                # Handle nested lists
                                elif isinstance(i, list) and len(i) == 1:
                                    my_dict[k] = iterate_dict(i[0], my_dict[k])
                                # Handle nested dictionaries
                                else:
                                    my_dict[k] = iterate_dict(i, my_dict[k])

                    # Handle dictionaries
                    else:
                        # Handle specific keys
                        if k == "attrs" or k == "in" or k == "out":
                            my_dict[k] = {}
                            for i in v:
                                if isinstance(i, dict):
                                    my_dict[k] = iterate_dict(i, my_dict[k])
                                else:
                                    my_dict[k] = i
                        elif isinstance(v, dict):
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v, my_dict[k])
                        else:
                            # Handle specific keys
                            if k == "description" or k == "notes" or k == "block_code":
                                v = ""
                            my_dict[k] = v
            except:
                raise

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
                return self.get_dictionary(json.load(file), my_dict)
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
            # Get the contents of the JSON file
            with open(self.filename, 'r', encoding='utf-8') as file:
                playbook_json = json.load(file)

            if "joint" in playbook_json["coa"]["data"]:
                # Analyze joint playbooks
                steps = playbook_json["coa"]["data"]["joint"]["cells"]
                name = os.path.splitext(os.path.basename(self.filename))[0]
                description = playbook_json["coa"]["data"]["description"].replace(
                    "\n\n", " ").replace("\n", "")
                tags = playbook_json["tags"]

                # Vendor
                analysis_dict.setdefault("vendor", []).append("Splunk")

                # Tags
                analysis_dict.setdefault("tags", []).append(tags)

                # Actuator
                actuators = [""] * len(steps)
                for i, step in enumerate(steps):
                    if "app" in step:
                        app = step["app"] if step["app"] != "" else ""
                        actuators[i] = app
                analysis_dict.setdefault("actuator", []).append(actuators)

                # Number of steps
                analysis_dict.setdefault("steps", []).append(len(steps))

                # Step types
                step_types = [step["type"] if "type" in step else "" for step in steps]
                analysis_dict.setdefault("step_types", []).append(step_types)

                # Step names
                step_names = [step["name"]  if "name" in step else "" for step in steps]
                analysis_dict.setdefault("step_names", []).append(step_names)

                # Playbook name
                analysis_dict.setdefault("playbook_name", []).append(name)

                # Playbook description
                analysis_dict.setdefault(
                    "playbook_description", []).append(description)

            else:
                # Analyze node-based playbooks
                steps = list(playbook_json["coa"]["data"]["nodes"].values())
                name = os.path.splitext(os.path.basename(self.filename))[0]
                description = playbook_json["coa"]["data"]["description"]
                tags = playbook_json["tags"]

                # Vendor
                analysis_dict.setdefault("vendor", []).append("Splunk")

                # Actuator
                actuators = [""] * len(steps)
                for i, step in enumerate(steps):
                    if "app" in step:
                        app = step["app"] if step["app"] != "" else ""
                        actuators[i] = app
                analysis_dict.setdefault("actuator", []).append(actuators)

                # Tags
                analysis_dict.setdefault("tags", []).append(tags)

                # Number of steps
                analysis_dict.setdefault("steps", []).append(len(steps))

                # Step types
                step_types = [step["type"] for step in steps]
                analysis_dict.setdefault("step_types", []).append(step_types)

                # Step names
                step_names = [step["data"]["functionName"] for step in steps]
                analysis_dict.setdefault("step_names", []).append(step_names)

                # Playbook name
                analysis_dict.setdefault("playbook_name", []).append(name)

                # Playbook description
                analysis_dict.setdefault(
                    "playbook_description", []).append(description)

            return analysis_dict

        except:
            raise
