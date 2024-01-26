# Module should take a list of logs and form a timeline of the logs
# It should be able to return an interactive timeline that is mutable
# Said time line can be export in different formats for preservation
# https://dadoverflow.com/2021/08/17/making-timelines-with-python/

from datetime import datetime
from LogThoth.Timeline import Activity
from LogThoth.Timeline.Event import Logon


class Creation(Activity): # Event ID 4688
    def __init__(self, RID: int, timestamp: datetime, file: str, logon: Logon) -> None:
        super().__init__(RID, timestamp)
        self.file = file
        self.logon = logon
        
class Termination(Activity): # Event ID 4689
    def __init__(self, RID: int, timestamp: datetime, file: str, logon: Logon) -> None:
        super().__init__(RID, timestamp)
        self.file = file
        self.logon = logon 


if __name__ == '__main__':
    # lol there is nothing to do
    pass
