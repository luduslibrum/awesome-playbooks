# CrowdStrike Yara Rules Ingest
## Summary
This Playbook runs on a timer trigger to reach out to CrowdStrike's Falcon Intelligence Rules API, download the latest set of Yara rules, and create them as signatures within the ThreatConnect platform. In addition to storing the rule itself, the description and version number of the Yara rule are extract and added as attributes.


## Dependencies
- Valid CrowdStrike Falcon Intelligence subscription and API access


## Input parameters
The Component requires the following configuration parameters:
- **CrowdStrike Falcon Intelligence API ID**: Your CrowdStrike Falcon Intelligence API ID.

- **CrowdStrike Falcon Intelligence API Secret Key**: Your CrowdStrike Falcon Intelligence API Secret Key.


## Output parameters
N/A


For more information on CrowdStrike Falcon Intelligence service, please refer to [https://www.crowdstrike.com/endpoint-security-products/falcon-x-threat-intelligence/](https://www.crowdstrike.com/endpoint-security-products/falcon-x-threat-intelligence/)