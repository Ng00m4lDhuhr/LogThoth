"""
an interface to easily access xml data as if it was fully deserialized in a data structure
"""
from interface.system import windows

class event(object):

    """ a class that acts as an interface to the etree of evtlogs records """

    ns = {"e": "http://schemas.microsoft.com/win/2004/08/events/event"}

    def __init__(self, record:object):
        self._record  = record
        self._data : dict = {}

    def __str__(self) -> str:
        return f"<record:{self.rid} machine:{self.computer} channel:{self.channel}>"

    def __hash__(self) -> str:
        # record id is unique per channel, also 2 records from same channel 
        # can have same record id from different windows device thus leaving 
        # the hash consisting of computer:channel:record id
        return f"{self.computer}:{self.channel}:{self.rid}"

    # Event Record Property

    @property
    def id(self) -> int:
        """The EventID property."""
        return int(self._record.find(".//e:EventID", namespaces=self.ns).text)
    
    @property
    def time(self):
        """The TimeCreated property."""
        # TODO choose a time structure and stick to it
        return self._record.find(".//e:TimeCreated", namespaces=self.ns).get("SystemTime")

    @property
    def computer(self):
        """The Computer property."""
        return self._record.find(".//e:Computer", namespaces=self.ns).text

    @property
    def channel(self):
        """The Channel property."""
        return self._record.find(".//e:Channel", namespaces=self.ns).text

    @property
    def rid(self):
        """The record id property."""
        return int(self._record.find(".//e:EventRecordID", namespaces=self.ns).text)

    def data(self, ValueName:str) -> object:
        try: return self._data[str(ValueName)]
        except KeyError:
            data_elements = record.findall(".//e:Data", namespaces=self.ns)
            for data in data_elements:
                self._data[data.get("Name")] = data.text
        try: return self._data[str(ValueName)]
        except KeyError: return None


class _logon(event):
    """
    class to ease access to EventData of logon attempts 
    """

    def __str__(self) -> str:
        return f"<machine={self.computer}/user={self.username} logonid={self.id} type={self.type}>"

    @property
    def username(self) -> str:
        """The target username property."""
        return self.data("TargetUserName")
    
    @property
    def logonType(self) -> (int,str):
        """The LogonType property."""
        return int(self.data("LogonType"))   
    
    @property
    def logonID(self) -> int:
        """The target logon id property."""
        return int(self.data("TargetLogonId"), 16)

    @property
    def process(self) -> str:
        """the process authenticating a user"""
        return self.data("ProcessName")

    @property
    def ip(self) -> str:
        """source ip address"""
        return self.data("IpAddress")

    @property
    def port(self) -> str:
        """source ip port"""
        return self.data("IpPort")

    @property
    def pid(self) -> int: 
        """the process id authenticating as user"""
        return int(self.data("ProcessId"), 16)


class evt4624(_logon):
    """
    class to ease access to EventData of successful logon attempts 
    see https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
    """
     
    def __init__(self, record:object):
        super().__init__(record)
        if self.id != 4624: 
            raise ValueError(f"Unexpected Event: given EventId is {self.id} expected 4624")


class evt4625(_logon):
    """
    a class to ease access to EventData of failed logon attempts
    see https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
    """

    def __init__(self, record:object):
        super().__init__(record)
        if self.id != 4625: 
            raise ValueError(f"Unexpected Event: given EventId is {self.id} expected 4625")
        
    @property
    def status(self) -> int:
       """status translation of failure reason"""
       pass

    @property 
    def substatus(self) -> int: 
        """substatus translation of failure reason"""
        return int( self.data(SubStatus), 16 )


def classify(record:object) -> event:
    """ function that decides the type of a log entry """
    if   4624 == int(record.find(".//e:EventID", namespaces=event.ns).text): return evt4624(record)
    elif 4625 == int(record.find(".//e:EventID", namespaces=event.ns).text): return evt4625(record)
    # TODO
    # elif 4688 == int(record.find(".//e:EventID", namespaces=event.ns).text): pass
    # elif 4689 == int(record.find(".//e:EventID", namespaces=event.ns).text): pass
    else: return event(record) # idk idc

