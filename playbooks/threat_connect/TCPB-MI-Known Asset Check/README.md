# Known Asset Check

The purpose of this playbook is to check to see if a newly created host or address indicator belongs to the user's organization. It does this by checking the indicator against WebSite Assets in the a Victim in ThreatConnect. Therefore there are a few configuration and setup requirements before this playbook will be usable.

## Setup Requirements

1. Create a Victim in the Org or another owner to use with this playbook.
1. For each IP address and hostname that you wish to alert on, create an Victim Asset of type WebSite in the above Victim.
1. Create a keychain variable in the Org's variable list for the Slack API token.

## Configuration

1. In the playbook trigger action settings, select all the owners this playbook will check for known assets on creation.
1. In the app "Get Victim", change the "Group Name" input parameter to the name of the Victm created for this playbook above.
1. In the same app, change the Owner parameter to the owner where the above Victim is located.
1. In the app "Send Alert", change the "Slack API Recipient" to the user or channel that will recieve Slack alerts.
1. In the same app, configure the "Slack API Token" input parameter with the keychain variable created above.

## Usage

Once activated, if a host or address is created in an owner checked by this playbook, it will be checked against all Victim assets. If the host or address is found in the Victim assets, a slack message about this will be sent.
