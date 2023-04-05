# Summary

Read a Google Alerts RSS feed and create indicators from the links. This playbook pulls the content from an RSS feed of Google alerts, finds the URLs from the alerts, and creates those URLs as indicators in ThreatConnect.

# Dependencies

n/a

# Use Cases

Once in a while, there is a Google search that turns up a lot of malicious or compromised domains. When this happens, it is helpful to use [Google Alerts](https://www.google.com/alerts) to create an RSS feed of websites matching the search. This playbook will then read from this RSS feed and create all of the urls as indicators in ThreatConnect. There are details and instructions for setting up an RSS feed for a Google alert here: [https://thenextweb.com/google/2013/09/11/google-alerts-regains-rss-delivery-option-it-lost-after-google-readers-demise/](https://thenextweb.com/google/2013/09/11/google-alerts-regains-rss-delivery-option-it-lost-after-google-readers-demise/).
