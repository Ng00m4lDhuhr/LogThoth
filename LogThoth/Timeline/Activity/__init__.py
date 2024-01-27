# Module should save logs parameters that we are interested in security wise
# The values within would be displayed in the UI
from datetime import datetime
                    
class Activity(object):
    # a representation of windows logged activity
    # this is an abstract class that defines the minimal
    # data we should aquire from a windows event log object
    # This class should symbolize the building blocks of a timeline
    def __init__(self,RID:int, timestamp:datetime) -> None:
        # It derives it's value and parameters from the raw log
        # This one is an abstract class that should save EventRecordID
        self.RID = RID
        self.time = timestamp

    def is_before(self, time:datetime) -> bool:
        return self.time < time

    def is_after(self, time:datetime) -> bool:
        return time < self.time

    def __eq__(self, other) -> bool:
        return self.RID == other.RID

    def __lt__(self, other) -> bool:
        return self.RID < other.RID

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __gt__(self, other) -> bool:
        return self.RID > other.RID

    def __ge__(self, other) -> bool:
        return self > other or self == other
    

if __name__ == '__main__':
    # lol there is nothing to do
    pass
