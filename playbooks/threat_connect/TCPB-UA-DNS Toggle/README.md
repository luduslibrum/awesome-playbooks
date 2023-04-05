# Summary

These playbooks allow users to turn on or off the DNS for all indicators associated with a group. It uses the process of collecting, serializing, and processing described [here](https://fhightower.gitbooks.io/threatconnect-playbook-paradigms-and-constructs/content/constructs/collect_serialize_process.html).

## Usage

Install all three of these playbooks and then install the array serializer playbook. Then edit the "Set Variable 1" app near the beginning of both the "Turn DNS Off Trigger" and "Turn DNS On Trigger" playbooks; you will need to provide the trigger link to the array serializer and the processing playbook (which is the "Adjust DNS" playbook in this case).

# Dependencies

- Array Serializer Playbook
