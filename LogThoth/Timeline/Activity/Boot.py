from LogThoth.Timeline import Activity
from datetime import datetime
from win32apievtlog import PyEventLogRecord

# System Event ID 27 signals boot type (it was successful) 
class PowerUp(Activity): 
    def __init__(self, log: PyEventLogRecord) -> None:
        super().__init__(log)

# System Event ID 1074 indicate process initiated shutdown
class Shutdown(Activity): 
    def __init__(self, log: PyEventLogRecord) -> None:
        super().__init__(log)

# TODO : track OS crashes
# System Event ID 41 indicate system crash
class Crash(Activity): 
    def __init__(self, log: PyEventLogRecord) -> None:
        super().__init__(log)
