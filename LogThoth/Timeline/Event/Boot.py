from Timeline import Event
from Timeline import Activity

class Boot(Event): 
    def __init__(self, start:Activity, end:Activity) -> None:
        super().__init__(start, end)
