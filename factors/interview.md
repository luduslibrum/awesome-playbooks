Incident Response Processes: Interview
=====================================

This interview aims to examine the modifications of incident response processes across organizations. It is applicable to researchers, cybersecurity professionals, and others interested in incident response. The questionnaire consists of the following sections:

1.      Research Idea
2.      Demographics (Organization)
3.      Incident Response Basics
4.      Playbooks
5.      Incident Response Scenarios

Participants are encouraged to ask for clarification whenever they find something unclear. The aggregated or anonymized responses will be used for scientific publication.

Research Idea
-------------

Organizations are affected by cyberattacks and conduct incident response. Typically, incident response processes across organizations have a common basis. However, due to various reasons organizations deviate and implement organization-specific processes. This questionnaire aims to examine modifications of incident response processes.

In the following, we use the term incident to broadly refer to any violation of the confidentiality, integrity, or availability of information or systems.

Demographics (Organization)
---------------------------

*       Please specify the size of your organization in terms of the number of employees.
*       Please specify the size of your organization's cybersecurity team(s) in terms of the number of employees working on cybersecurity topics.
*       Please specify the size of your incident response team(s) in terms of the number of employees working on incident response.
*       Does your organization have multiple cybersecurity teams? If so, please list them.
*       Please specify the maturity of your cybersecurity team(s) including technology and processes. What is the basis for your self-assessment?

Incident Response Basics
------------------------

*       Does your organization perform incident response with only ad-hoc methods, or do you use defined incident response processes (BPMN or textual)?
*       Does your organization use generic security process descriptions (e.g., BPMN, NIST Incident Response Life Cycle, NIST Cybersecurity Framework, FIRST CSIRT Framework, etc.) or incident response maturity models (e.g., SIM3, etc.) or incident response standards (e.g., CACAO, OpenC2, RE&CT, MITRE D3FEND, etc.) or Security Orchestration, Automation and Response (SOAR) tools (e.g., Splunk Phantom, Cortex XSOAR, Tines, etc.) or an incident response policy to define guiding principles?
*       Is your organization interested in automating incident response processes, comparing/benchmarking incident response processes, and transferring knowledge on incident response processes?
*       What is the most important aspect of incident management/response for your organization? Technology, People, or Processes?
*       What is your incident definition? When does an alert/alarm become an incident?

Playbooks
---------

*       Does your organization have playbooks? If so, how many, and how do you define the term "playbook"? Which types of incidents are covered by playbooks?
*       How do you describe your playbooks? How detailed are your playbooks (processes vs. procedures)?
*       What is your opinion on sharing and using shared playbooks? Do you see the potential that playbooks will be shared in the future?
*       How did you create your playbooks? Did you have templates from tools, gather information from public sources, or build them on existing organization-specific processes?

Incident Response Scenarios
---------------------------

This section contains three scenarios. Participants are requested to provide a brief description of their incident response processes for each scenario and answer follow-up questions.

### Ransomware

Your organization's network has been infiltrated. Ransomware was downloaded and installed. There are encrypted files on multiple computers. The attackers demand a $50k ransom to decrypt the files and threaten to publish confidential information (double extortion).

*       How does your organization handle a ransomware scenario? Please provide a brief description of your process steps.
*       Is the incident response process the same for different types of incidents/attacks?
*       How does your organization handle this scenario differently than other organizations? Please provide a brief description and justification of specifics)
*	    What would your organization do differently if …
    *       … it is a publicly traded company in the United States?
    *       … it has customers in the European Union?
    *       … it has proxy log retention is set to 1 week only? 
    *       … it observed compromised email accounts?
    *       … it has a dedicated Cyber Threat Intelligence team?
    *       … it defined an incident budget of $100k?
    
### DDoS

Your organization is experiencing a distributed denial-of-service attack against its main web server and email server. The attackers are using a botnet and simultaneously request server resources causing benign requests to be dropped. This leads to unavailable services and causes financial losses.

*	    How does your organization handle a DDoS scenario? Please provide a brief description of your process steps.
*	    How does your organization handle this scenario differently than other organizations? Please provide a brief description and justification of specifics.
*	    What would your organization do differently if …
    *       … it is a sub-contractor for the defense industry?
    *       … it has defined email for incident response communication?
    *       … it has sourced server hosting to a third-party?
    *       … it has business-critical applications running on the targeted web server?
    *       … it has a security team with 100 security experts?
    *       … it has a Web Application Firewall and additional server capacity?

### APT

Your organization is the target of a sophisticated attacker group. The attackers have gained privileged access to your network and moved laterally. In a next step they attempt to exfiltrate confidential information and destroy industrial control systems.

*	    How does your organization handle an APT scenario? Please provide a brief description of your process steps.
*       How does your organization handle this scenario differently than other organizations? Please provide a brief description and justification of specifics.
*	    What would your organization do differently if …
    *       … … it is operating in Israel?
    *       … … it assumes a state-sponsored attacker group located in Iran behind the attack?
    *       … … it has defined formal reporting requirements?
    *       … … it has specified to contact the CISO, but CISO is unavailable?	
    *       … … its CFO’s laptop is affected?
    *       … … it has specified incident response time limits for APT attacks to 1 month?


Any other business
---------------------------

*       Any open topics you would like to discuss?

*       Do you see merit in analyzing influential factors for incident response?

Thank you
---------------------------
*	    Thank you for your time!
*	    Plan to publish the results in a scientific journal or at a conference
*	    Research results (interested: yes/no?)
