from LogThoth.Timeline import Activity
from datetime import datetime

class PowerUp(Activity): # Event ID 12
    def __init__(self, RID: int, timestamp: datetime) -> None:
        super().__init__(RID, timestamp)

class Shutdown(Activity): # Event ID 13
    def __init__(self, RID: int, timestamp: datetime) -> None:
        super().__init__(RID, timestamp)