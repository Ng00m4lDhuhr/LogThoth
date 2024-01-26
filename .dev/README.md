# Software Architecture
## Serializer Module
Highly optimized single threading module with minimal form of parsing. It's functionality is mapping [PyEventLogRecord](https://timgolden.me.uk/pywin32-docs/PyEventLogRecord.html) to [LogThoth.Timeline.Activity](https://github.com/Ng00m4lDhuhr/LogThoth/blob/main/Timeline.py#L8) and creating meaningful [LogThoth.Timline.Event](https://github.com/Ng00m4lDhuhr/LogThoth/blob/main/Timeline.py#L56)s. 
## User Interface
Single-threading or Multi-threading module that present. The final goal is to create a presentable interactive timeline object for user to comprehend.
