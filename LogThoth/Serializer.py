import win32evtlog
from Timeline.Event import *
from enum import Enum

class LogType(Enum):
    SETUP = 'Setup'
    SYSTEM = 'System'
    SECURITY = 'Security'
    APP = 'Application'

# Get Event By id
def read_event_logs(EventID:list,log_type:str) -> list:
    # Open the specified event log
    handle = win32evtlog.OpenEventLog(None, log_type)
    # Set the read flags so that it reads first
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    # Read all events
    Events_list = []
    events = 1
    while events:
        events = win32evtlog.ReadEventLog(handle, flags, 0)
        for event in events:
            if event.EventID in EventID:
                Events_list.append(event)             
    # Close the event log
    win32evtlog.CloseEventLog(handle)
    return Events_list
        
######################
## Query Functions
######################

def GetBootEvents() -> list:
    Boot = []
    # TODO : read logs sequentially backwards (old --> future) once as the following (if you see applicable)
    EventRecords = read_event_logs([12,13],LogType.SYSTEM)
    if EventRecords[0].id == 13 : EventRecords = EventRecords[1::] # Skips a ShutDown without a previous PowerUp
    EventRecords = EventRecords[0::-1]  # skips the current PowerUp as we know what is happening rn
    for up, down in EventRecords : Boot += Boot(up,down)
    return Boot

def GetLogonEvents(bootEvent: Event) -> list: 
    # Query User login in Boot duration
    # Return list of Logon object
    pass

def GetExecutionEvents(logonEvent: Event) -> list:
    # Query Processes execution and termination in duration of login
    # Return list of Binary object
    pass

if __name__ == "__main__":
    boot = GetBootEvents()



