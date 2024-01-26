from LogThoth.Timeline import Event
from LogThoth.Timeline.Activity import Process

class Execution(Event):
    def __init__(self, start: Process.Creation, end: Process.Termination):
        super().__init__(start, end)
        