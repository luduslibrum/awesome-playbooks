<h1>About these Workflows</h1>
These workflows are triggered when a SolarWinds alert is received by Ayehu NG stating that IIS is down.  They then take the following steps:
<ul>
<li>They create a record in the ITSM system (either ServiceNow or Cherwell)</li>
<li>Query the status of the IIS service on the remote host</li>
<li>If the service is down, it is brought back up, and if it's not down, the ticket is updated accordingly</li>
<li>If the service is successfully brought back up, the SolarWinds alert is acknowledged and the ticket is updated, and if not, the ticket is updated accordingly</li>
</ul>

<b>Find a video tutorial on this workflow here:</b> <a href="https://www.youtube.com/watch?v=qIALL8_F6v8">https://www.youtube.com/watch?v=qIALL8_F6v8</a>
