# Module should take a logs and store relevant information in format it in meaningful manner

from datetime import datetime
from LogThoth.Timeline import Activity
from LogThoth.Timeline.Event import Logon


# Security Event ID 4688 indicate a creation of process
class Creation(Activity): 
    def __init__(self, RID: int, timestamp: datetime, file: str, logon: Logon) -> None:
        super().__init__(RID, timestamp)
        self.file = file
        self.logon = logon
        
# Security Event ID 4689 indicate a termination of process
class Termination(Activity): 
    def __init__(self, RID: int, timestamp: datetime, file: str, logon: Logon) -> None:
        super().__init__(RID, timestamp)
        self.file = file
        self.logon = logon 


if __name__ == '__main__':
    # lol there is nothing to do
    pass