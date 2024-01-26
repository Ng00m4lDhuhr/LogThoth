from LogThoth.Timeline import Event
from LogThoth.Timline.Activity import User

class Login(Event): # a duration where a certain user logged in and logged out
    def __init__(self, start:User.Login, end:User.Logout) -> None:
        # this should record the start time , the end time, and the username and SID
        super().__init__(start, end)