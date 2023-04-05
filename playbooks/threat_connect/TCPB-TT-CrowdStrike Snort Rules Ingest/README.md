# CrowdStrike Snort Rules Ingest
## Summary
This Playbook runs daily on a timer trigger to reach out to CrowdStrike's Falcon Intelligence Rules API, download the latest set of Snort rules, and create them as signatures within the ThreatConnect platform. In addition to storing the rule itself, the report number of the report associated to the Snort rule is extracted and added as a tag. Additionally the version number is added as an attribute.


## Dependencies
- Valid CrowdStrike Falcon Intelligence subscription and API access


## Input parameters
The Component requires the following configuration parameters:
- **CrowdStrike Falcon Intelligence API ID**: Your CrowdStrike Falcon Intelligence API ID.

- **CrowdStrike Falcon Intelligence API Secret Key**: Your CrowdStrike Falcon Intelligence API Secret Key.


## Output parameters
N/A


For more information on CrowdStrike Falcon Intelligence service, please refer to [https://www.crowdstrike.com/endpoint-security-products/falcon-x-threat-intelligence/](https://www.crowdstrike.com/endpoint-security-products/falcon-x-threat-intelligence/)
