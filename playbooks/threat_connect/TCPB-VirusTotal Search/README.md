Summary

This playbook utilizes a search term for VirusTotals premium API /search endpoint. Once that data is returned, the file hashes are stored in ThreatConnect. The query is set in the 'Set Query and Tag Term' step. Both of those will also be applied as tags for easy management and data filtering.

Dependencies

VirusTotal premium API key. This needs to be set in both HTTP clients as a header parameter: key=x-apikey, value=API key