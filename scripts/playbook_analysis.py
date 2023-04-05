import argparse
import json
import logging
import os

from vendor.catalyst import Catalyst
from vendor.demisto import Demisto
from vendor.fortinet import Fortinet
from vendor.iacd import IACD
from vendor.logic_hub import LogicHub
from vendor.msazure import MSAzure
from vendor.oasis_open import OasisOpen
from vendor.rapid7 import Rapid7
from vendor.resolve import Resolve
from vendor.shuffle import Shuffle
from vendor.chronicle import Chronicle
from vendor.splunk import Splunk
from vendor.threatconnect import ThreatConnect
from vendor.cisa import CISA
from vendor.tines import Tines
from vendor.xsoar import Xsoar

# Configure logging
logger = logging.getLogger('playbook analysis')
ch = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Define a list of supported platforms
platforms = [
    "xsoar", "fortinet", "tines", "logichub", "oasisopen", "shuffle", "chronicle",
    "splunk", "catalyst", "demisto", "resolve", "rapid7", "threatconnect", "msazure", "iacd", "cisa"
]


class PlaybookAnalysis:
    """
    A class to analyze vendor-specific playbooks according to certain parameters
    """

    def __init__(self, platform: str, path: str):
        # Make sure the platform is in the list of supported platforms
        if platform.lower() not in platforms:
            raise ValueError(f"{platform.upper()} platform is not implemented. "
                             f"Please try one of the following platforms: {platforms}")

        self.platform = platform.lower()
        self.path = path

    def run(self):
        """
        Run analysis for either a file or directory
        """
        # Create an empty dictionary to hold the results
        results = {}

        # If the path is a file, transform it
        if os.path.isfile(self.path):
            self._analyze_file(self.path, results)

        # If the path is a directory, transform all files in it
        elif os.path.isdir(self.path):
            for root, dirs, files in os.walk(self.path):
                for file in files:
                    logger.info(f"Processing file: {file}")
                    file_path = os.path.join(root, file)
                    self._analyze_file(file_path, results)

        # Otherwise, do nothing
        else:
            pass

        # Output array length
        logger.info(", ".join([f"{key}: {len(value)}" for key, value in results.items()]))

        # Write the results to a file
        with open(f"../analysis/vendor/{self.platform}.py", "w", encoding="utf8") as file:
            json.dump(results, file)

    def _analyze_file(self, filename, my_dict):
        """
        Trigger platform-specific analysis for a file

        :param filename: str, the name of the file to analyze
        :param my_dict: dict, the dictionary to update with the analyzed data
        :return: tuple, a dictionary with the updated data and a boolean indicating if the file format is supported
        """

        # get the platform from the instance variable
        platform = self.platform

        # initialize the switch to True
        switch = True

        # switch based on the platform
        # use try-except block to handle unsupported platform
        try:
            # create a handler instance for the platform
            handler = None
            if platform == "xsoar":
                handler = Xsoar(filename)
            elif platform == "fortinet":
                handler = Fortinet(filename)
            elif platform == "tines":
                handler = Tines(filename)
            elif platform == "logichub":
                handler = LogicHub(filename)
            elif platform == "oasisopen":
                handler = OasisOpen(filename)
            elif platform == "shuffle":
                handler = Shuffle(filename)
            elif platform == "chronicle":
                handler = Chronicle(filename)
            elif platform == "splunk":
                handler = Splunk(filename)
                with open(filename, 'r', encoding='utf-8') as file:
                    playbook_json = json.load(file)
                    if "custom_function_id" in playbook_json:
                        switch = False
            elif platform == "catalyst":
                handler = Catalyst(filename)
            elif platform == "demisto":
                handler = Demisto(filename)
            elif platform == "resolve":
                handler = Resolve(filename)
            elif platform == "rapid7":
                handler = Rapid7(filename)
            elif platform == "iacd":
                handler = IACD(filename)
            elif platform == "cisa":
                # check if the file format is supported
                if filename.endswith("bpmn"):
                    handler = CISA(filename)
                else:
                    # if not, set switch to False
                    switch = False
            elif platform == "threatconnect":
                if filename.endswith("pbx"):
                    handler = ThreatConnect(filename)
                else:
                    switch = False
            elif platform == "msazure":
                if filename.endswith("json"):
                    with open(filename, 'r', encoding='utf-8') as file:
                        playbook_json = json.load(file)
                        if "resources" not in playbook_json:
                            switch = False
                    handler = MSAzure(filename)
                else:
                    switch = False

            # call the map_values method of the handler and update my_dict
            if handler is not None and switch:
                my_dict = handler.analyze_playbook(my_dict)
                
        except NotImplementedError:
            # set switch to False if the platform is not supported
            switch = False


        # return the updated dictionary and the switch
        return my_dict, switch


if __name__ == "playbookAnalysis._analyze_file":
    # print error message if this module is imported
    logger.error(
        "This converter is currently meant to be used as a CLI tool only.")
    logger.error(
        "Use 'python3 -m playbook2Schema._analyze_file -h' in your console for additional help.")

if __name__ == '__main__':
    # create an argument parser and add arguments
    parser = argparse.ArgumentParser(
        description="A vendor-specfic playbook analysis exporter.")
    # required arguments
    parser.add_argument(
        "--platform", "-v", help="The origin of the playbooks (SOAR platform), e.g., Cortex.", required=True)
    parser.add_argument(
        "--path", "-p", help="Path to a file or directory of playbooks.", required=True)
    parser.add_argument("--log-level", "-l", help="Log level.", required=True)

    # parse the arguments from command line
    args = parser.parse_args()

    # set log level
    logger.setLevel(args.log_level)
    ch.setLevel(args.log_level)
    
    try:
        # initialize the playbooksAnalysis object and analyze the playbooks
        logger.debug('Start transformation of playbooks')
        transformator = PlaybookAnalysis(args.platform, args.path)
        transformator.run()
    except KeyboardInterrupt:
        # handle the keyboard interrupt exception
        logger.info("Received KeyboardInterrupt, exiting...")

