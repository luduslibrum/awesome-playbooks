# Deploy Yara Rule to CarbonBlack
## Summary
This Playbook will allow a user deploy a Yara rule to Carbon Black's Yara Manager. The Playbook uses a User Action Trigger which presents a button on the Details page of Signature groups that, when pressed, will gather the contents of the Signature and SCP them over via SSH to the host running the Yara Manager. SSH is required because there is currently no API endpoint for uploading Yara rules.

## Dependencies
- Carbon Black Yara Manager
- Valid SSH credentials

## Input parameters
The Playbook requires the following configuration parameters:
- **SSH Hostname**: The host that the Carbon Black Yara Manager is running on,

- **SSH Username**: The username of the user with SSH permissions.

- **SSH Password**: The password of the user with SSH permissions.

- **SSH Port**: The port that SSH is running on (by default this is set to 22).

NOTE: The Playbook is configured to allow you to enter the SSH Hostname, Username, and Password information during the import process and will save them as Org Variables.


## Output Variables
N/A


For more information on Carbon Black's Yara Manager, please refer to [https://developer.carbonblack.com/guide/enterprise-response/cb-yara-manager-guide/](https://developer.carbonblack.com/guide/enterprise-response/cb-yara-manager-guide/)