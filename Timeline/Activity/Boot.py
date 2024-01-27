from LogThoth.Timeline import Activity
from datetime import datetime

# System Event ID 32 signals boot type (it was successful) 
class PowerUp(Activity): 
    def __init__(self, RID: int, timestamp: datetime) -> None:
        super().__init__(RID, timestamp)

# System Event ID 1074 indicate process initiated shutdown
# System Event ID 41 indicate system crash
class Shutdown(Activity): 
    def __init__(self, RID: int, timestamp: datetime) -> None:
        super().__init__(RID, timestamp)
