from LogThoth.Timeline import Event
from LogThoth.Timline import Activity

class Boot(Event): 
    def __init__(self, start:Activity, end:Activity) -> None:
        super().__init__(start, end)
