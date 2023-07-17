Awesome Playbooks [](https://github.com/luduslibrum/awesome-playbooks)
=============================================================

[![Percentage of issues still open](http://isitmaintained.com/badge/open/luduslibrum/awesome-playbooks.svg)](http://isitmaintained.com/project/luduslibrum/awesome-playbooks "Percentage of issues still open")
[![GitHub forks](https://img.shields.io/github/forks/luduslibrum/awesome-playbooks)](https://github.com/luduslibrum/awesome-playbooks/network)
[![GitHub stars](https://img.shields.io/github/stars/luduslibrum/awesome-playbooks)](https://github.com/luduslibrum/awesome-playbooks/stargazers)

> A curated repository of **1347 playbooks** and scripts for security incident response, aimed to help security analysts and [DFIR](http://www.acronymfinder.com/Digital-Forensics%2c-Incident-Response-%28DFIR%29.html) teams.

| Vendor | Playbooks | Format | Link |
| --- | --- | --- | --- |
| Catalyst | 3 | YAML | [/playbooks/catalyst](playbooks/catalyst) |
| Cortex XSOAR | 131 | YAML | [/playbooks/xsoar](playbooks/xsoar) |
| Cisa IR playbooks | 81 | BPMN | [/playbooks/cisa](playbooks/cisa) |
| Palo Alto Demisto | 59 | YAML | [/playbooks/demisto](playbooks/demisto) |
| Fortinet FortiSOAR | 193 | JSON | [/playbooks/fortinet](playbooks/fortinet) |
| Guardsight | 55 | PDF | [/playbooks/guard\_sight](playbooks/guard_sight) |
| IACD Automate | 9 | BPMN | [/playbooks/iacd\_automate](playbooks/iacd_automate) |
| LogicHub SOAR | 70 | JSON | [/playbooks/logichub](playbooks/logichub) |
| Microsoft | 4 | PNG | [/playbooks/microsoft](playbooks/microsoft) |
| MS Azure Sentinel | 217 | JSON | [/playbooks/ms\_azure](playbooks/ms_azure) |
| OasisOpen | 1 | JSON | [/playbooks/oasis\_open](playbooks/oasis_open) |
| Rapid7 Insightconnect | 214 | ICON | [/playbooks/rapid7](playbooks/rapid7) |
| Resolve | 149 | XML | [/playbooks/resolve](playbooks/resolve) |
| Shuffle Automation | 18 | JSON | [/playbooks/shuffle](playbooks/shuffle) |
| Chronicle Security | 4 | JSON | [/playbooks/siemplify](playbooks/chronicle) |
| Splunk SOAR | 119 | JSON | [/playbooks/splunk](playbooks/splunk) |
| ThreatConnect | 83 | PBX(Z) | [/playbooks/threat\_connect](playbooks/threat_connect) |
| Tines | 87 | JSON | [/playbooks/tines](playbooks/tines) |

Methodology
-----------

In addition, we provide a structural and content analysis of the playbooks and their steps. On the one hand, we look at the schemas of individual vendors and derive a meta-playbook from them ([go to schemas](schemas/)). In addition, we analyze the content of the playbooks, compare the steps, and form categories ([go to analysis](analysis/)).

![methodoloy](https://user-images.githubusercontent.com/23430598/220401059-145d38f1-df7b-4bea-83b0-f45098a22282.svg)

Influencing Factors
-------

We conducted expert interviews with nine experts and performed an online study with n=147 to gather information on a incident response processes. The data collected is not published to protect the privacy of the participants, but we publish the structure and content of both the interview and the questionnaire ([go to factors](factors/)).


Citation
-------

Please consider citing our publication if you are using our **Awesome-Playbooks** for your research: 

```bib
@InProceedings{Schlette2023,
author = {Daniel Schlette and 
		  Philip Empl and 
		  Marco Caselli and
		  Thomas and 
		  G{\"u}nther Pernul}, 
title = {Do You Play It by the Books? A Study on Incident Response Playbooks and Influencing Factors},
booktitle = {Proceedings of the 45th IEEE Symposium on Security and Privacy, {SP} 2024, San Francisco, CA, USA, May 20-23, 2024},
pages = {1--19},
publisher = {{IEEE}},
year={2024}
}
```