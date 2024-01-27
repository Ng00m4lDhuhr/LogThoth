from datetime import datetime
from LogThoth.Timeline import Activity
from win32apievtlog import PyEventLogRecord

class Login(Activity): # Event ID 4624
    def __init__(self, log: PyEventLogRecord) -> None:
        super().__init__(log)
        self.logonID = log.Data # should somehow find a way to parse data
        self.SID = log.Data # should somehow find a way ot parse data
        self.username = log.Data # should somehow find a way to parse data
  
class Logout(Activity): # Event ID 4634
    
    def __init__(self, log: PyEventLogRecord) -> None:
        super().__init__(log)
        self.logonID = log.Data # should somehow find a way to parse data
        self.SID = log.Data # should somehow find a way ot parse data
        self.username = log.Data # should somehow find a way to parse data
