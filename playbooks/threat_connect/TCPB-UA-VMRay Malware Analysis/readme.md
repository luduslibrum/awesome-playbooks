# VMRay Playbooks

The first playbook - VMRay Submission - submits malware to VMRay and saves the sample and submission ID
as attributes to the original triggering item. Additionally it will tag the malware as “vmray-processing”.

The second playbook - VMRay Get Results - will retrieve and parse the results from VMRay and associate them to the triggering malware. It will also change the tag to “VMRay Processed” so that a user has a visual indication that it has been submitted and processed.

## App Dependencies
2 custom attributes:
`VMRay Sample ID`
`VMRay Submission ID`

## Use Cases
Submit malware for analysis to VMRay and get the results from VMRay.
