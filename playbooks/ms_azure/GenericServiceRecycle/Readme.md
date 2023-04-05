# GENECRIC SERVICE STOP REMIDIATION:

## Restart Windows ,Linux  SERVICE  if a monitored SERVICE goes down.

This use case is able to restrat service of both os 

* Linux
* WINDOWS

### REQUIRED INPUT

* 1.HOSTNAME : Taken from incidnet
* 2.SERVICE NAME : Taken from Incident

NOTE: FOR THIS USE CASE SERVICE NOW ITSM TICKET IS USED TO TRIGGER YOU CAN MAKE CHANGES ACCORIDING TO YOUR REQUIREMENT 



ACTION:


* 1.this workflow check service status 
* 2.Restart the stopped service
* 3.put required details in tickes
* 4.on succesfull ticket will close
* 5.on failure reassign mechanism will trigger.

