# Parse STIX XML 
This playbook is intended to parse a STIX XML file from the File Post spaces app.  See https://kb.threatconnect.com/customer/portal/articles/2920045 for how to configure and use the File Post app. 

Once the playbook receives a file from the File Post app it will run the file through the STIX Parser playbook app and then import the data in ThreatConnect with the ThreatConnect Import app.  Additionally, it can save the uploaded file as a Document and associate the file to the indicators and groups that were created.  Results are returned to the user in the HTTP response.  
