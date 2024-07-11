"""
Each event log has enough info to understand the context of the record
This code should provide a container that encompasses all the logs within a defined context
"""


class context(object):
    """virtual class to define contexts"""
    pass


class session(context):
    """object to identify a session"""
    def __init__(self, sid:str, host:str, logonId:int, username:str=None):
        self.lid = int(logonId)             # live unique session id
        self.sid = str(sid)             # user identifier
        self.username = username or ''  # current username
        self.host = str(host)           # hosting machine identifier


class execution(context):
    """object to identify a program execution"""
    def __init__(self,  pid:int, image:str):
        self.image = str(image)
        self.pid = int(pid)


