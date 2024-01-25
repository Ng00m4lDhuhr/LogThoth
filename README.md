![some kickass logo](https://github.com/Ng00m4lDhuhr/LogThoth/blob/main/Logo.png?raw=true)
# LogThoth : Super Targeted Timeline Tool
the goal of this project is to automate logs filteration processes for incident responders and digital forensics investigators. The tool functionality is separated in 3 different parts, each cooperate to enhance the analysis process.

## Software Components
### Serializer
The component is acting as a middle ground between LogThoth [Timeline Module](https://github.com/Ng00m4lDhuhr/LogThoth/blob/main/README.md#timeline) application and Windows Event Logs, creating events to add to a generated timeline. 
### Timeline
As a core module that defines interesting events and activities that are proven valuable in security investigations.
### User Interface
Transforms the python3 modules from functions to a tool that is usable from terminal or GUI alike.

References
---
* Article: [Learning win32evtlog in python](https://ph20eow.gitbook.io/tech-stuff/silketw/learning-win32evtlog-in-python)
* Docs: [win32evtlog module](https://timgolden.me.uk/pywin32-docs/win32evtlog.html)
* Docs: [EventLogRecord Object](https://timgolden.me.uk/pywin32-docs/PyEventLogRecord.html)
* Docs: [Windows Event Log 4624](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4624)
