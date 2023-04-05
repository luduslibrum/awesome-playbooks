# Recorded Future - IOC - Enrichment
author: Adrian Porcescu, Recorded Future

This playbook leverages the Recorded Future API to automatically enrich the IP, Domain, Url and Hash indicators, found in incidents, with the following Recorded Future context: Risk Score, Risk Rules and Link to Intelligence Card. The enrichment content will be posted as a comment in the Sentinel incident. For additional information please visit [Recorded Future](https://www.recordedfuture.com/integrations/azure/) 

Links to deploy the RecordedFuture_IOC_Enrichment playbook template:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2FAzure-Sentinel%2Fmaster%2FPlaybooks%2FRecordedFuture_IOC_Enrichment%2FRecordedFuture_IOC_Enrichment.json)
[![Deploy to Azure Gov](https://aka.ms/deploytoazuregovbutton)](https://portal.azure.us/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2FAzure-Sentinel%2Fmaster%2FPlaybooks%2FRecordedFuture_IOC_Enrichment%2FRecordedFuture_IOC_Enrichment.json)