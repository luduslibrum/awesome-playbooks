import xmltodict
import json
import re

class Resolve():
    """
    A playbook transformation class. Converts Resolve-specific playbooks into a JSON schema.
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

        # iterate through the items in the json_object dictionary
        for k, v in json_object.items():

            # if the value is a list
            if isinstance(v, list):

                # if the list has only one entry, e.g., key : []
                if len(v) == 0:
                    if k not in my_dict:
                        my_dict[k] = []

                # if the list contains only one key, e.g., key : ['brandinstances']
                elif len(v) == 1:
                    my_dict[k] = {}
                    my_dict[k] = self.get_dictionary(v[0], my_dict[k])

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

            # if the value is not a list
            else:
                # HERE IS THE MAIN DIFFERENCE FOR EACH VENDOR
                if k == "tasks":
                    my_dict[k] = {}
                    for i in v:
                        my_dict[k] = self.get_dictionary(v[str(i)], my_dict[k])
                elif isinstance(v, dict):
                    my_dict[k] = {}
                    my_dict[k] = self.get_dictionary(v, my_dict[k])
                elif k not in my_dict:
                    my_dict[k] = v

        # return the updated dictionary object
        return my_dict

    def map_values(self, my_dict={}) -> dict:
        """
        Load a YAML file and return a dictionary with mapped values.

        Args:
        - filename (str): Path to the YAML file.

        Returns:
        - dict: A dictionary with mapped values.
        """
        # Open the XML file and read its content
        with open(self.filename, 'r', encoding='utf-8') as file:
            # Convert the XML to a JSON string and parse it into a Python dictionary
            playbook_dict = json.loads(json.dumps(
                xmltodict.parse(file.read()), indent=4))
            # Use the get_dictionary() method to process the dictionary and return the result
            return self.get_dictionary(playbook_dict, my_dict)

    def check_key(self, dictionary, steps):
        # iterate over each key-value pair in the dictionary
        for key, value in dictionary.items():
            # if the value is a dictionary and it is not one of these specific keys
            if isinstance(value, dict) and key != "IfElseActivity" and key != "WhileActivity" and key != "ParallelActivity":
                # if the value is a dictionary with a specific key format
                if isinstance(value, dict):
                    if "ns" in key or "@" not in key:
                        # extract the name and actuator from the dictionary and add it to the list
                        name = value["@name"] if "ns" not in key else key.split(":")[
                            1]
                        actuator = value["@TargetModuleName"] if "@TargetModuleName" in value else ""
                        steps.append(
                            {"name": name, "type": "Activity", "actuator": actuator})
                else:
                    # if the value is not a dictionary, append it to the list
                    steps.append(value[0])

            # if the key is "IfElseActivity"
            elif key == "IfElseActivity":
                # append information about the gateway to the list
                steps.append({"name": "IfElseActivity",
                             "type": "Gateway", "actuator": ""})
                if isinstance(value, dict):
                    # recursively call the function with the value of this key
                    steps = self.check_key(value, steps)
                else:
                    # iterate over the list of dictionaries and call the function for each
                    for val in dictionary["IfElseActivity"]:
                        for val2 in val["IfElseBranchActivity"]:
                            steps = self.check_key(val2, steps)

            # if the key is "WhileActivity"
            elif key == "WhileActivity":
                # append information about the loop to the list
                steps.append({"name": "WhileActivity",
                             "type": "Loop", "actuator": ""})
                if isinstance(value, dict):
                    # recursively call the function with the value of this key
                    steps = self.check_key(value["SequenceActivity"], steps)
                else:
                    # iterate over the list of dictionaries and call the function for each
                    for val in dictionary["WhileActivity"]:
                        steps = self.check_key(val["SequenceActivity"], steps)

            # if the key is "ParallelActivity"
            elif key == "ParallelActivity":
                # append information about the parallel activity to the list
                steps.append({"name": "ParallelActivity",
                             "type": "Parallel", "actuator": ""})
                for val in dictionary[key]["SequenceActivity"]:
                    # iterate over the list of dictionaries and call the function for each
                    steps = self.check_key(val, steps)
        return steps

    def analyze_playbook(self, analysis_dict) -> dict:
        """
        Analyzes the YAML playbook and updates the provided dictionary with the extracted values.

        Args:
        - analysis_dict: A dictionary object to update with extracted values.

        Returns: 
        - A dictionary object.
        """

        try:
            # Open the playbook file
            with open(self.filename, 'r', encoding='utf-8') as file:
                # Convert the XML file to JSON
                playbook_json = json.loads(json.dumps(
                    xmltodict.parse(file.read()), indent=4))

                # Get the sequential workflow activity from the playbook JSON and extract the steps
                flows = json.loads(json.dumps(xmltodict.parse(
                    playbook_json["TotalExport"]["Workflows"]["WorkflowInfo"]["@Xoml"]), indent=4))
                steps = []
                steps = self.check_key(
                    flows["SequentialWorkflowActivity"], steps)

                # Extract the playbook name and description
                name = playbook_json["TotalExport"]["Workflows"]["WorkflowInfo"]["@Name"]
                description = playbook_json["TotalExport"]["Workflows"]["WorkflowInfo"]["@Description"]

                # Extract the list of tags
                tags = []
                if "playbookLabels" in playbook_json:
                    if len(playbook_json["playbookLabels"]) != 0:
                        for label in playbook_json["playbookLabels"]:
                            tags.append(label["playbookLabelType"]["label"])

                # Add the extracted information to the analysis dictionary
                analysis_dict.setdefault("actuator", []).append(
                    [task["actuator"] for task in steps])
                analysis_dict.setdefault("vendor", []).append("Resolve")
                analysis_dict.setdefault("tags", []).append(tags)
                analysis_dict.setdefault("steps", []).append(len(steps))
                analysis_dict.setdefault("step_types", []).append(
                    [step["type"] if "type" in step else "" for step in steps])
                analysis_dict.setdefault("step_names", []).append(
                    [" ".join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', step["name"])).split()) if "name" in step else "" for step in steps])
                analysis_dict.setdefault("playbook_name", []).append(name)
                analysis_dict.setdefault(
                    "playbook_description", []).append(description)

                return analysis_dict

        except:
            raise
