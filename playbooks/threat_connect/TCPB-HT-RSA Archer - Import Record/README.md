# RSA Archer | Import Archer Record
This playbook starts with an HTTP Trigger which is intended to be triggered by an Archer advanced workflow.  Once triggered, the playbook will download and parse the Archer record based with the ID that was passed to it.  From there it will create a ThreatConnect Incident and save the  parsed fields in the Incident.  Additionally, it will parse the Actor saved on the Archer record and either save or associated it to the Incident in ThreatConnect.  Lastly, the Archer record is updated with the link back to the Incident in ThreatConnect. 

