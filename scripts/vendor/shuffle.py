import json


class Shuffle():
    """
    A playbook transformation class. Converts Shuffle-specific playbooks into a JSON schema.
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
        Recursively converts a Shuffle-specific playbook into a JSON schema.

        Args:
        - json_object (dict): The Shuffle-specific playbook to be converted.
        - my_dict (dict): The resulting JSON schema. Used for recursion.

        Returns:
        - dict: The resulting JSON schema.
        """

        # A recursive function to iterate through the dictionary
        def iterate_dict(json_object, my_dict={}) -> dict:

            try:
                # Iterate through each key-value pair in the JSON object
                for k, v in dict(json_object).items():

                    # Handle lists
                    if isinstance(v, list):
                        # Handle empty list
                        if len(v) == 0:
                            # If the key is not already in the dictionary, add it with an empty dictionary as its value
                            if k not in my_dict:
                                my_dict[k] = {}

                        # Handle list with one entry
                        elif len(v) == 1:
                            # If the value is a dictionary, add it to the key in the dictionary
                            if isinstance(v[0], dict):
                                my_dict[k] = {}
                                my_dict[k] = iterate_dict(v[0], my_dict[k])
                            # Otherwise, add the value to the key in the dictionary
                            else:
                                my_dict[k] = v

                        # Handle list with one nested list
                        elif isinstance(v[0], list) and k not in my_dict and len(v[0]) == 1:
                            my_dict[k] = iterate_dict(v[0][0])

                        # Handle list with a nested dictionary
                        elif isinstance(v[0], dict) and k not in my_dict:
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v[0], my_dict[k])

                        # Handle list with multiple entries
                        else:
                            if k not in my_dict:
                                my_dict[k] = {}
                                for i in v:
                                    if isinstance(i, str) or isinstance(i, int) or isinstance(i, bool):
                                        my_dict[k] = i
                                    elif isinstance(i, list) and len(i) == 1:
                                        my_dict[k] = iterate_dict(
                                            i[0], my_dict[k])
                                    else:
                                        my_dict[k] = iterate_dict(
                                            i, my_dict[k])

                    # Handle non-list values
                    else:
                        # Handle specific keys differently
                        if k == "steps" or k == "sync_features" or k == "categories":
                            my_dict[k] = {}
                            for i in v:
                                if isinstance(i, dict):
                                    my_dict[k] = iterate_dict(i, my_dict[k])
                                else:
                                    my_dict[k] = i
                        # Handle nested dictionary
                        elif isinstance(v, dict):
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v, my_dict[k])
                        # Handle special cases
                        else:
                            if k == "large_image" or k == "image":
                                v = ""
                            my_dict[k] = v

            # Handle any exceptions
            except Exception as e:
                print(f"Exception while iterating: {e}")

            # Return the resulting dictionary
            return my_dict

        # Call the recursive function and return the resulting dictionary
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
            # Open the playbook JSON file and load its contents
            with open(self.filename, 'r', encoding='utf-8') as file:
                playbook_json = json.load(file)

                # Call the get_dictionary function to extract the values and map them to the analysis_dict dictionary
                return self.get_dictionary(playbook_json, my_dict)
        except:
            # Raise any exceptions that occurred during the processing
            raise

    def analyze_playbook(self, analysis_dict) -> dict:
        """
        Analyzes the JSON playbook and updates the provided dictionary with the extracted values.

        Args:
        - analysis_dict: A dictionary object to update with extracted values.

        Returns: 
        - A dictionary object.
        """

        with open(self.filename, 'r', encoding='utf-8') as f:
            playbook = json.load(f)

            # vendor
            analysis_dict.setdefault("vendor", []).append("Shuffle")

            # tags
            tags = playbook.get("tags", [])
            analysis_dict.setdefault("tags", []).append(tags)

            # create a list of actuators from playbook actions list
            actuators = [task.get("app_name", "") if task.get("category", "") != "Testing" else "" for task in playbook["actions"]]
            analysis_dict.setdefault("actuator", []).append(actuators)

            # number of steps
            analysis_dict.setdefault("steps", []).append(
                len(playbook["actions"]))

            # step types
            step_types = [step.get("label", "")
                          for step in playbook["actions"]]
            analysis_dict.setdefault("step_types", []).append(step_types)

            # step names
            step_names = [str(" ".join(step["name"].split("_"))) if "name" in step else "" for step in playbook["actions"]]
            analysis_dict.setdefault("step_names", []).append(step_names)

            # playbook name
            analysis_dict.setdefault(
                "playbook_name", []).append(playbook["name"])

            # playbook description
            description = playbook.get("description", "").split("\n\n")[0]
            analysis_dict.setdefault(
                "playbook_description", []).append(description)

        return analysis_dict
