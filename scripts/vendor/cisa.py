import xmltodict
import json


class CISA():
    """
    A playbook transformation class. Converts CISA Automate-specific playbooks into a JSON schema.
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
        Recursively converts a CISA-specific playbook into a JSON schema.

        Args:
            json_object (dict): The CISA-specific playbook to be converted.
            my_dict (dict): The resulting JSON schema. Used for recursion.

        Returns:
            dict: The resulting JSON schema.
        """        
        
        for k, v in json_object.items():
            # handle values that are lists
            if isinstance(v, list):
                # handle empty lists
                if len(v) == 0:
                    if k not in my_dict:
                        my_dict[k] = []
                # handle lists that contain only one value
                elif len(v) == 1:
                    my_dict[k] = {}
                    my_dict[k] = self.get_dictionary(v[0], my_dict[k])
                # handle lists that contain one nested list
                elif isinstance(v[0], list) and k not in my_dict and len(v[0]) == 1:
                    my_dict[k] = self.get_dictionary(v[0][0])
                # handle lists that contain multiple dictionaries or lists
                else:
                    if k not in my_dict:
                        my_dict[k] = {}
                    for i in v:
                        if isinstance(i, str):
                            my_dict[k] = i
                        elif isinstance(i, list) and len(i) == 1:
                            my_dict[k] = self.get_dictionary(i[0], my_dict[k])
                        else:
                            my_dict[k] = self.get_dictionary(i, my_dict[k])
            else:
                # handle "tasks" key for each vendor
                if k == "tasks":
                    my_dict[k] = {}
                    for i in v:
                        my_dict[k] = self.get_dictionary(v[str(i)], my_dict[k])
                elif isinstance(v, dict):
                    my_dict[k] = {}
                    my_dict[k] = self.get_dictionary(v, my_dict[k])
                elif k not in my_dict:
                    my_dict[k] = v

        return my_dict

    def map_values(self, my_dict={}) -> dict:
        """
        Load a YAML file and return a dictionary with mapped values.

        Args:
        - filename (str): Path to the YAML file.

        Returns:
        - dict: A dictionary with mapped values.
        """
        
        # Open the file in read mode and use utf-8 encoding
        with open(self.filename, 'r', encoding='utf-8') as file:
            # Read the content of the file and parse it using xmltodict library
            playbook_dict = xmltodict.parse(file.read())
            # Convert the parsed content to JSON format using the json library
            playbook_json = json.dumps(playbook_dict, indent=4)
            # Parse the JSON content and return the resulting dictionary by calling the get_dictionary method
            return self.get_dictionary(json.loads(playbook_json), my_dict)


    def analyze_playbook(self, analysis_dict) -> dict:
        """
        Analyzes the YAML playbook and updates the provided dictionary with the extracted values.

        Args:
        - analysis_dict: A dictionary object to update with extracted values.

        Returns: 
        - A dictionary object.
        """

        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                # parse XML and convert to JSON
                playbook_json = json.loads(json.dumps(xmltodict.parse(file.read()), indent=4))

                # get the process name
                name = playbook_json["bpmn:definitions"]["bpmn:process"]["@name"]

                # get the step information
                steps = []
                for key, val in playbook_json["bpmn:definitions"]["bpmn:process"].items():
                    if "bpmn" in key and key != "bpmn:process" and key != "bpmndi:BPMNDiagram" and key != "bpmn:sequenceFlow" and key != "bpmndi:BPMNShape":
                        if isinstance(val, dict):
                            steps.append({
                                "name": val.get("@name", "").replace("\n\n", " "),
                                "type": val["@id"].split("_")[0],
                                "actuator": "Human" if key == "bpmn:userTask" else ""
                            })
                        else:
                            for v in val:
                                steps.append({
                                    "name": v.get("@name", "").replace("\n\n", " "),
                                    "type": v["@id"].split("_")[0],
                                    "actuator": "Human" if key == "bpmn:userTask" else ""
                                })

                # add data to analysis_dict
                analysis_dict.setdefault("vendor", []).append("CISA")
                analysis_dict.setdefault("actuator", []).append([s["actuator"] for s in steps])
                analysis_dict.setdefault("tags", []).append([])
                analysis_dict.setdefault("steps", []).append(len(steps))
                analysis_dict.setdefault("step_types", []).append([s["type"] if "type" in s else "" for s in steps])
                analysis_dict.setdefault("step_names", []).append([s["name"] if "name" in s else "" for s in steps])
                analysis_dict.setdefault("playbook_name", []).append(name)
                analysis_dict.setdefault("playbook_description", []).append("")

                return analysis_dict

        except Exception as e:
            raise e
