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
    index_event_1 = -1
    index_event_2 = -1
    result = []
    
    for i in range(len(timeEVT_1)):
        min = np.inf
        index_event_1 = -1
        index_event_2 = -1
        for j in range(len(timeEVT_2)):
            date_time1 = datetime.strptime(timeEVT_1[i], '%Y-%m-%d %H:%M:%S')
            date_time2 = datetime.strptime(timeEVT_2[j], '%Y-%m-%d %H:%M:%S')
            cmp = abs(date_time1.timestamp() - date_time2.timestamp())

            if cmp < min and date_time1 < date_time2:
                min = cmp
                index_event_1 = i
                index_event_2 = j

        if index_event_1 > -1 and index_event_2 > -1:
            result.append([timeEVT_1[index_event_1],timeEVT_2[index_event_2]])
    
    return result

def get_event_logs(query):
    c = wmi.WMI()

    # Query the Win32_NTLogEvent class for events with the specified Event ID

    events = c.query(query)

    event_list = []

    for event in events:

        event_list.append(event)

    return event_list

def CheckIsInteractive(evts):
    final_evts = []
    for event in evts:
        msgs = event.Message.split('\r\n')
        for msg in msgs:
            if "Logon Type" in msg:
                type = msg[-1]
                if msg[-1] == "2":
                    final_evts.append(event)
    return final_evts

def LoginCombine(LoginEvts,LogOffEvts):
    result = []
    for login in LoginEvts:
        for logoff in LogOffEvts:
            loginData = getData(login.Message)
            logoffData = getData(logoff.Message)
            if loginData["Logon ID"] == logoffData["Logon ID"] and loginData["Security ID"] == logoffData["Security ID"]:
                result.append([TimeFromat(login.TimeGenerated),TimeFromat(logoff.TimeGenerated)])
    return result

                
def getData(msg:str):
    data = {}
    msg = msg.split('\r\n')
    for value in msg:
        value = value.strip('\t')
        value = value.split(':')
        try:
            data[value[0]] = value[1].strip("\t")
        except IndexError:
            pass
    return data

                
def GetBoot():
    TimeEvt27 = []
    TimeEvt1074 = []
    evt_27 = get_event_logs(f"SELECT * FROM Win32_NTLogEvent WHERE EventCode = 27")
    evt_1074 = get_event_logs(f"SELECT * FROM Win32_NTLogEvent WHERE EventCode = 1074")

    for event in evt_27:
        TimeEvt27.append(TimeFromat(event.TimeGenerated))
    
    for event in evt_1074:
        TimeEvt1074.append(TimeFromat(event.TimeGenerated))
    
    BootTimeLine = Combine(TimeEvt27,TimeEvt1074)

    return BootTimeLine


def GetLogIn():
    FilterdEvt4624 = []
    FilterdEvt4647 = []
    evt_4624 = get_event_logs(f"SELECT * FROM Win32_NTLogEvent WHERE EventCode = 4624")
    evt_4647 = get_event_logs(f"SELECT * FROM Win32_NTLogEvent WHERE EventCode = 4647")

    for event in evt_4624:
        data = getData(event.Message)
        # if data["Logon Type"] == "2":
        if data["Security ID"].startswith("S-1-5-21"):
            FilterdEvt4624.append(event)
    
    for event in evt_4647:
        data = getData(event.Message)
        # if data["Logon Type"] == "2":
        if data["Security ID"].startswith("S-1-5-21"):
            FilterdEvt4647.append(event)

    # remove Duplicate
    # FilterdEvt4624 = list(set(FilterdEvt4624))
    # FilterdEvt4647 = list(set(FilterdEvt4647))
        
    LoginTimeLine = LoginCombine(FilterdEvt4624,FilterdEvt4647)

    return LoginTimeLine


Log = GetLogIn()

for i in Log:
    print(i[0]+"-"*10+i[1])
