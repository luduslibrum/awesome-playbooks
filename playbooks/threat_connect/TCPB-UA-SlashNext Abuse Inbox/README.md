# Overview
This Playbook provides the SlashNext Abuse Inbox URL Scan capabilities for the ThreatConnect platform. This Playbook specifically addresses the following scenario:

1) A suspected malicious email is forwarded to the mailbox associated with this Playbook.
2) The URLs from this message are extracted and de-duplicated.
3) Each URL is scanned using the SlashNext Phishing Incident Response App.
4) Malicious URLs are stored in the platform and a report is generated containing each malicious URL.
5) The original email content is stored and associated with the report that is generated.
6) Each malicious URL is created as an Indicator and associated with the report.
7) An in-platform notification is generated to review the report.
8) A response is sent back to the From address for the original email to indicate the status of the scan.

## Requirements
In order to make use of this Playbook, you will need to install the SlashNext Phishing Incident Response App into your instance of the ThreatConnect Platform. This app along with the documentation is available here: https://github.com/ThreatConnect-Inc/threatconnect-playbooks/tree/master/apps/SlashNext%20Phishing%20Incident%20Response