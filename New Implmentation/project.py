import wmi
from datetime import datetime
import numpy as np


def TimeFromat(time):
    date = time[:8]
    exact_time = time[8:14]
    formated_time = time[:4] +"-"
    for i in range(4,len(date),2):
        if i == len(date) - 2:
            formated_time += date[i:i+2] + " "
            continue
        formated_time += date[i:i+2] + "-"

    
    for i in range(0,len(exact_time),2):
        if i == len(exact_time) - 2:
            formated_time += exact_time[i:i+2]
            continue
        formated_time += exact_time[i:i+2] + ":"
    
    return formated_time

def Combine(timeEVT_1,timeEVT_2):
    min = np.inf
    index_event_1 = -1
    index_event_2 = -1
    result = []
    for i in range(len(timeEVT_1)):
        for j in range(len(timeEVT_2)):
            date_time1 = datetime.strptime(timeEVT_1[i], '%Y-%m-%d %H:%M:%S')
            date_time2 = datetime.strptime(timeEVT_2[j], '%Y-%m-%d %H:%M:%S')
            cmp = abs(date_time1 - date_time2)

            if cmp.total_seconds() < min and date_time1 < date_time2:
                min = cmp.total_seconds()
                index_event_1 = i
                index_event_2 = j

        result.append([timeEVT_1[index_event_1],timeEVT_2[index_event_2]])
    
    return result

def get_event_logs(event_id):
    c = wmi.WMI()

    # Query the Win32_NTLogEvent class for events with the specified Event ID
    query = f"SELECT * FROM Win32_NTLogEvent WHERE EventCode = {event_id}"
    events = c.query(query)

    event_list = []

    for event in events:
        # event_info = {
        #     "TimeGenerated": event.TimeGenerated,
        #     "Message": event.Message,
        # }
        event_list.append(event)

    return event_list



def GetBoot():
    tmpEvt27 = []
    tmpEvt1074 = []
    evt_27 = get_event_logs(27)
    evt_1074 = get_event_logs(1074)

    for event in evt_27:
        tmpEvt27.append(TimeFromat(event.TimeGenerated))
    
    for event in evt_1074:
        tmpEvt1074.append(TimeFromat(event.TimeGenerated))
    
    BootTimeLine = Combine(tmpEvt27,tmpEvt1074)

    return BootTimeLine


def GetLogIn():
    tmpEvt4624 = []
    tmpEvt4634 = []
    evt_4624 = get_event_logs(4624)
    evt_4634 = get_event_logs(4634)

    for event in evt_4624:
        tmpEvt4624.append(TimeFromat(event.TimeGenerated))
    
    for event in evt_4634:
        tmpEvt4634.append(TimeFromat(event.TimeGenerated))
    
    LoginTimeLine = Combine(tmpEvt4624,tmpEvt4634)

    return LoginTimeLine

# def GetBoot():
#     pass


Boot = GetBoot()

for event in Boot:
    print(event[0]+"-"*10+event[1])