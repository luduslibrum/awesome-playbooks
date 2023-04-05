# False Positive Triage Playbooks

You can view more documentation for these playbooks here: [https://tc.hightower.space/post/playbooks/false-positive-triage/](https://tc.hightower.space/post/playbooks/false-positive-triage/).

## Pre-5.7 Release

Everything in the `pre-5.7` directory will work in ThreatConnect versions before 5.7. The `pre-5.7/False Positive Triage Standalone - pre 5.7.pbx` playbook can be installed on its own and provides a user-action trigger to triage false positives. There are also two interfaces (`pre-5.7/False Positive Triage HTTP Interface.pbx` and `pre-5.7/False Positive Triage Trigger Interface.pbx`) which provide different interfaces with the false positive triage component [here](https://github.com/ThreatConnect-Inc/threatconnect-playbooks/tree/master/components/false-positive-triage). The advantage of this structure (as described [here](https://pb-constructs.hightower.space/playbooks/paradigms/structuring-playbook-systems)) is that it is more flexible and interface-agnostic.

## Post-5.7 Release

Everything in the `post-5.7` directory will only work in ThreatConnect versions after the release of version 5.7.
