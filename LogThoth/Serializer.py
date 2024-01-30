import win32evtlog
from Timeline.Event import *
from enum import Enum

LogType = ['Setup','System','Security','Application']

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
    boot = []
    # TODO : read logs sequentially backwards (old --> future) once as the following (if you see applicable)
    EventRecords = read_event_logs([27,1074],LogType[1])
    
    if EventRecords[0].EventID == 27 : 
        EventRecords = EventRecords[1::] # Skips a ShutDown without a previous PowerUp
    
    for i in range(0,len(EventRecords),2) :
        boot += Event.Boot.Boot(EventRecords[i].EventID,EventRecords[i+1].EventID)

    return boot

def GetLogonEvents() -> list: 
    logon = []
    # TODO : read logs sequentially backwards (old --> future) once as the following (if you see applicable)
    EventRecords = read_event_logs([4624,4634],LogType[1])
    # Do we really need to remove the first EVENT?!!
    if EventRecords[0].EventID == 4624 : 
        EventRecords = EventRecords[1::] # Skips a ShutDown without a previous PowerUp

    for i in range(0,len(EventRecords),2) :
        logon += Event.Logon.Login(EventRecords[i].EventID,EventRecords[i+1].EventID)

    return boot

def GetExecutionEvents(logonEvent: Event) -> list:
    binary = []
    # TODO : read logs sequentially backwards (old --> future) once as the following (if you see applicable)
    EventRecords = read_event_logs([4688,4689],LogType[1])
    
    for i in range(0,len(EventRecords),2) :
        binary += Event.Execution.Binary(EventRecords[i].EventID,EventRecords[i+1].EventID)

    return boot

if __name__ == "__main__":
    boot = GetBootEvents()



