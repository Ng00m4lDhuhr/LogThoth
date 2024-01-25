# Module should take a list of logs and form a timeline of the logs
# It should be able to return an interactive timeline that is mutable
# Said time line can be export in different formats for preservation
# https://dadoverflow.com/2021/08/17/making-timelines-with-python/

from datetime import datetime
                    
class Activity(object):
    # a representation of windows logged activity
    # this is an abstract class that defines the minimal
    # data we should aquire from a windows event log object
    # This class should symbolize the building blocks of a timeline
    def __init__(self,RID:int, timestamp:datetime) -> None:
        # It derives it's value and parameters from the raw log
        # This one is an abstract class that should save EventRecordID
        pass

    def __eq__(self, other) -> bool:
        return self.RID == other.RID

class UserLogin(Activity):
    def __init__(self, RID: int, timestamp: datetime, logonID:int, SID:str, username) -> None:
        super().__init__(RID, timestamp)
        self.logonID = logonID
        self.SID = SID
        self.username = username
        
  
class UserLogout(Activity):
    def __init__(self, RID: int, timestamp: datetime, logonID:int, SID:str, username) -> None:
        super().__init__(RID, timestamp)
        self.logonID = logonID
        self.SID = SID
        self.username = username

class PowerUp(Activity):
    def __init__(self, RID: int, timestamp: datetime) -> None:
        super().__init__(RID, timestamp)

class Shutdown(Activity): 
    def __init__(self, RID: int, timestamp: datetime) -> None:
        super().__init__(RID, timestamp)

class Process(Activity):
    def __init__(self, RID: int, timestamp: datetime) -> None:
        # Use PID, SID, LOGON ID as identifier
        super().__init__(RID, timestamp)
        
class Connection(Activity):
    def __init__(self, RID: int, timestamp: datetime) -> None:
        # Refer to the process creating this ID by PID, SID, and LOGON ID
        super().__init__(RID, timestamp)
    


class Event(object): 
    # an object that symbolize the an event that has a non-zero duration
    # and can be elicitated from 2 windows event logs. One that refers
    # to it's beginning the other denotes that it ended. 
    def __init__(self, start:Activity, end:Activity) -> None:
        self.stime = start
        self.etime = end

class Boot(Event): 
    def __init__(self, start:PowerUp, end:Shutdown) -> None:
        super().__init__(start, end)
        
class Login(Event): 
    def __init__(self, start:UserLogin, end:UserLogout) -> None:
        # this should record the start time , the end time, and the username and SID
        super().__init__(start, end)



class Timeline(object):
    # class that should represent a timeline
    # it contain an time ordered list of Event objects
    def __init__(self) -> None:
        pass



if __name__ == '__main__':
    # lol there is nothing to do
    pass
