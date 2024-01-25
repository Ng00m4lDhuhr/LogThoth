import win32evtlog
from itertools import chain
import string
import time
import re
import Timeline

class LogStack(object):
    
    LOG_TYPES = ['Setup','System','Security', 'Application']
    
    def __init__(self):
        pass

    def date2sec(self,evt_date:str) -> int:

        '''

        converts '12/23/99 15:54:09' to seconds

        print '333333',evt_date

        '''

        regexp=re.compile('(.*)\\s(.*)')

        reg_result=regexp.search(evt_date)

        date=reg_result.group(1)

        the_time=reg_result.group(2)

        (mon,day,yr)=map(lambda x: string.atoi(x),string.split(date,'/'))

        (hr,min,sec)=map(lambda x: string.atoi(x),string.split(the_time,':'))

        tup=[yr,mon,day,hr,min,sec,0,0,0]

        sec=time.mktime(tup)

        return sec
    

    def __repr__(self):
        return {self.type: self.event}
    
    # Union operation of event if types are the same
    def __add__(self, other): 
        pass
    # remove intersected events if types are the same
    def __sub__(self, other): 
        pass
    
    # logical operators for time comparison
    # should compare earliest events in the stacks
    def __eq__(self, other) -> bool:
        pass
    def __gt__(self, other) -> bool: 
        pass
    def __lt__(self, other) -> bool: 
        pass
    def __le__(self, other) -> bool: 
        pass
    def __ge__(self, other) -> bool: 
        pass

    def sort(events:list) -> list:
        output = []
        sec = []
        for event in events:
            sec.append(date2sec(event.TimeGenerated.Format()))

        sorted_sec = sec.sort()
        
        for i in range(len(sorted_sec)):
            indices = [j for j, x in enumerate(sec) if x == sorted_sec[i]]
            for index in indices:
                output.append(events[index])

    
# 6005,6006,6013
                
    def GetPowerUp(self,log_type:str):
        return self.read_event_logs([12],log_type)

    def GetShutDown(self,log_type:str):
        return self.read_event_logs([13],log_type)

    def GetUserLogin(self,log_type:str):
        return self.read_event_logs([4624],log_type)

    def GetUserLogout(self,log_type:str):
        return self.read_event_logs([4647],log_type)
    
    def GetProcess(self,log_type:str):
        return self.read_event_logs([4688],log_type)
    
    # def GetConnection(self):
    #     return self.read_event_logs(["4624"])


    def GetBootEvent(self,log_type:str)-> list:
        PowerUp = self.GetPowerUp(log_type)
        ShutDown = self.GetShutDown(log_type)
        Boot = []
        for i in range(len(PowerUp)-1):

            Boot.append(Timeline.Boot(PowerUp[i+1],ShutDown(i)))
        
        return Boot
        

    @staticmethod
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

            
            # for event in events:
            #    print(f"Event Name: {event.EventType}")
            #    print(f"Time Generated: {event.TimeGenerated.Format()}")
            #    print(f"Event ID: {event.EventID}")
            #    print(f"Event Source: {event.SourceName}")
            #    print(f"Event Category: {event.EventCategory}")
            #    print(f"Event Data: {event.StringInserts}")
            #    print("-" * 50)

        # Close the event log
        win32evtlog.CloseEventLog(handle)
        return Events_list



if __name__ == "__main__":
    # Specify the log type [e.g., 'System', 'Security', 'Application']
    # Logs.read_event_logs('Setup')
    LogTypes = ['System', 'Security', 'Application','Setup']
    stack = LogStack()
    boot = stack.GetBootEvent(LogTypes[0])



