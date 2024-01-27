# Module should provide an abstract of logs as an interesting event
# It should be utilized to define a set of logs yet not load or directly
# refer to said logs implicitly within it's parameters

from datetime import datetime
from Logthoth.Timeline import Activity

class Event(object): 
    # an object that symbolize the an event that has a non-zero duration
    # and can be elicitated from 2 windows event logs. One that refers
    # to it's beginning the other denotes that it ended. 
    def __init__(self, start:Activity, end:Activity) -> None:
        self.stime = start
        self.etime = end


if __name__ == '__main__':
    # lol there is nothing to do
    pass
