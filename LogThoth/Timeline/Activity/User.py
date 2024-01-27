from datetime import datetime
from LogThoth.Timeline import Activity


class Login(Activity): # Event ID 4624
    def __init__(self, RID: int, timestamp: datetime, logonID:int, SID:str, username) -> None:
        super().__init__(RID, timestamp)
        self.logonID = logonID
        self.SID = SID
        self.username = username        
  
class Logout(Activity): # Event ID 4634
    def __init__(self, RID: int, timestamp: datetime, logonID:int, SID:str, username) -> None:
        super().__init__(RID, timestamp)
        self.logonID = logonID
        self.SID = SID
        self.username = username
