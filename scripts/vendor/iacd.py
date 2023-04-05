import xmltodict
import json


class IACD():
    """
    A playbook transformation class. Converts IACD Automate-specific playbooks into a JSON schema.
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
        Recursively converts a IACD-specific playbook into a JSON schema.

        Args:
            json_object (dict): The IACD-specific playbook to be converted.
            my_dict (dict): The resulting JSON schema. Used for recursion.

        Returns:
            dict: The resulting JSON schema.
        """

        # A recursive function to iterate through the dictionary
        def iterate_dict(json_object, my_dict={}) -> dict:

            try:
                # Iterate through key-value pairs of dictionary
                for k, v in json_object.items():
                    # if the value is a list
                    if isinstance(v, list):
                        # if list is empty, add empty list to the key in the dictionary
                        if len(v) == 0:
                            if k not in my_dict:
                                my_dict[k] = []
                        # if list contains only one element, recursively add it to the dictionary under the key
                        elif len(v) == 1:
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v[0], my_dict[k])
                        # if the list contains a single nested list, recursively add it to the dictionary under the key
                        elif isinstance(v[0], list) and k not in my_dict and len(v[0]) == 1:
                            my_dict[k] = iterate_dict(v[0][0])
                        # if the nested object is a dictionary, recursively add it to the dictionary under the key
                        elif isinstance(v[0], dict) and k not in my_dict:
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v[0], my_dict[k])
                        # if the list contains multiple dictionaries or lists, recursively add each element to the dictionary under the key
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
                    # if the value is not a list, add it to the dictionary under the key
                    else:
                        if isinstance(v, dict):
                            my_dict[k] = {}
                            my_dict[k] = iterate_dict(v, my_dict[k])
                        elif k not in my_dict:
                            my_dict[k] = v
            # Catch any exceptions raised during iteration and print error message
            except Exception as e:
                print(f"Error iterating through {k} : {v}")
                print(f"Exception: {e}")
            # Return the dictionary
            return my_dict
        
        # Call the recursive function and return the resulting dictionary
        return iterate_dict(json_object, my_dict)


    def map_values(self, my_dict={}) -> dict:
        """
        Load a YAML file and return a dictionary with mapped values.

        Args:
        - filename (str): Path to the YAML file.

        Returns:
        - dict: A dictionary with mapped values.
        """
        # Open the file for reading and specify the encoding
        with open(self.filename, 'r', encoding='utf-8') as file:
            # Convert the XML data to JSON format and pretty-print it
            playbook_json = json.dumps(xmltodict.parse(file.read()), indent=4)
            # Extract the data from the JSON object and store it in a dictionary
            return self.get_dictionary(json.loads(playbook_json), my_dict)


    def analyze_playbook(self, analysis_dict) -> dict:
        """
        Analyzes the YAML playbook and updates the provided dictionary with the extracted values.

        Args:
        -  analysis_dict: A dictionary object to update with extracted values.
        
        Returns: 
        - A dictionary object.
        """

        try:
            # Open the file and load the XML data as JSON string
            with open(self.filename, 'r', encoding='utf-8') as file:
                playbook_json = json.dumps(xmltodict.parse(file.read()), indent=4)
            
            # Load the JSON string as a Python dictionary
            playbook_json = json.loads(playbook_json)

            # Extract information from the playbook JSON
            step_names = []
            step_types = []
            actuators = []
            tags = []
            description = ""
            name = playbook_json["bpmn:definitions"]["bpmn:process"].get("@name", "")

            # If the name is not defined, set it as the name of the file without extension and underscores
            if name == "":
                # If name is empty
                name = self.filename # Convert filename from bytes to string
                name = name.split("\\")[-1] # Extract file name from path
                name = name.split(".")[0] # Split file name by period and take first part
                name = name.replace("_", " ") # Replace underscores with spaces

            # Iterate over the process keys to extract steps information
            for key in playbook_json["bpmn:definitions"]["bpmn:process"]:
                if "bpmn" in key and key not in ["bpmn:process", "bpmndi:BPMNDiagram", "bpmn:sequenceFlow", "bpmndi:BPMNShape"]:
                    if isinstance(playbook_json["bpmn:definitions"]["bpmn:process"][key], dict):
                        # If the key value is a dictionary
                        if "@name" in playbook_json["bpmn:definitions"]["bpmn:process"][key]:
                            # If the dictionary has a "name" attribute, append it to the step_names list
                            step_names.append(playbook_json["bpmn:definitions"]["bpmn:process"][key]["@name"].replace("\n\n", " "))
                            step_types.append(playbook_json["bpmn:definitions"]["bpmn:process"][key]["@id"].split("_")[0])
                            actuators.append("")
                        else:
                            # If the dictionary has no "name" attribute, append an empty string to the step_names list
                            step_names.append("")
                            step_types.append(playbook_json["bpmn:definitions"]["bpmn:process"][key]["@id"].split("_")[0])
                            actuators.append("")
                    else:
                        # If the key value is a list, iterate over the values to extract the steps information
                        for val in playbook_json["bpmn:definitions"]["bpmn:process"][key]:
                            if "@name" in val:
                                step_names.append(val["@name"].replace("\n\n", " "))
                                step_types.append(val["@id"].split("_")[0])
                                actuators.append("")
                            else:
                                step_names.append("")
                                step_types.append(val["@id"].split("_")[0])
                                actuators.append("")
            
            # Update the analysis_dict dictionary with the extracted information
            analysis_dict.setdefault("vendor", []).append("IACD")
            analysis_dict.setdefault("actuator", []).append(actuators)
            analysis_dict.setdefault("tags", []).append(tags)
            analysis_dict.setdefault("steps", []).append(len(step_names))
            analysis_dict.setdefault("step_types", []).append(step_types)
            analysis_dict.setdefault("step_names", []).append(step_names)
            analysis_dict.setdefault("playbook_name", []).append(name)
            analysis_dict.setdefault("playbook_description", []).append(description)

            return analysis_dict

        except:
            # Raise any exception that occurs during the execution
            raise
