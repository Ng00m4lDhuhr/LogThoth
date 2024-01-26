![some kickass logo](https://github.com/Ng00m4lDhuhr/LogThoth/blob/main/Graphics/Logo.png)
# LogThoth : Super Targeted Timeline Tool
the goal of this project is to automate logs filteration processes for incident responders and digital forensics investigators in the analysis cycle. The tool functionality is separated in 3 different components, each cooperate to enhance the analysis process of log viewing in a siemless environment.

## Components
### Serializer
The component is acting as a middle ground between LogThoth [Timeline Module](https://github.com/Ng00m4lDhuhr/LogThoth/blob/main/#timeline) application and Windows Event Logs, creating events to add to a generated timeline. 
### Timeline
As a core module that defines interesting events and activities that are proven valuable in security investigations.
### User Interface
Transforms the python3 modules from code to a usable tool that is usable from terminal or GUI alike.

References
---
* **Docs**: [Windows EventLog Auditing](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4624)
* **Docs**: [Windows EventLogRecord Class](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.eventing.reader.eventlogrecord?view=dotnet-plat-ext-7.0)
* **Article**: [Learning win32evtlog in Python](https://ph20eow.gitbook.io/tech-stuff/silketw/learning-win32evtlog-in-python)
* **Docs**: [Win32evtlog Module](https://timgolden.me.uk/pywin32-docs/win32evtlog.html)
* **Docs**: [EventLogRecord Object](https://timgolden.me.uk/pywin32-docs/PyEventLogRecord.html)
