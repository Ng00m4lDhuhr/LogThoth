import wmi
import yara
import hashlib
import numpy as np
from datetime import datetime
from colorama import Fore, Style, init

init(convert=True)
RULE_PATH = "C:\\Users\\user\\Desktop\\LogThor Project\\rules\\"

def yara_detection(path):
    keylogger_rule = yara.compile(RULE_PATH+"MALW_viotto_keylogger.yar")
    try:
        matches = keylogger_rule.match(path)
        if matches: return True
    except: pass
    return False

def banner():
    print(Fore.GREEN+"""
 #       #######  #####           ####### #     # ####### ####### #     # 
 #       #     # #     #             #    #     # #     #    #    #     # 
 #       #     # #                   #    #     # #     #    #    #     # 
 #       #     # #  ####    #####    #    ####### #     #    #    ####### 
 #       #     # #     #             #    #     # #     #    #    #     # 
 #       #     # #     #             #    #     # #     #    #    #     # 
 ####### #######  #####              #    #     # #######    #    #     # 
"""+Style.RESET_ALL) 

def TimeFormat(time):
    date = time[:8]
    exact_time = time[8:14]
    formatted_time = time[:4] +"-"
    for i in range(4,len(date),2):
        if i == len(date) - 2:
            formatted_time += date[i:i+2] + " "
            continue
        formatted_time += date[i:i+2] + "-" # formatted time
    
    for i in range(0,len(exact_time),2):
        if i == len(exact_time) - 2:
            formatted_time += exact_time[i:i+2]
            continue
        formatted_time += exact_time[i:i+2] + ":"
    return formatted_time

def Combine(EVT_1,EVT_2):
    result = []
    
    for i in range(len(EVT_1)):
        min = np.inf
        index_event_1 = -1
        index_event_2 = -1
        timeEVT_1 = -1
        timeEVT_2 = -1
        for j in range(len(EVT_2)):
            TMPtimeEVT_1 = TimeFormat(EVT_1[i].TimeGenerated)
            TMPtimeEVT_2 = TimeFormat(EVT_2[j].TimeGenerated)

            date_time1 = datetime.strptime(TMPtimeEVT_1, '%Y-%m-%d %H:%M:%S')
            date_time2 = datetime.strptime(TMPtimeEVT_2, '%Y-%m-%d %H:%M:%S')
            cmp = abs(date_time1.timestamp() - date_time2.timestamp())

            if cmp < min and date_time1 < date_time2:
                min = cmp
                index_event_1 = i
                index_event_2 = j
                timeEVT_1 = TMPtimeEVT_1
                timeEVT_2 = TMPtimeEVT_2

        if index_event_1 > -1 and index_event_2 > -1:
            result.append([EVT_1[index_event_1],timeEVT_1])
            # result.append([EVT_1[index_event_1],timeEVT_1,EVT_2[index_event_2],timeEVT_2])

        else:
            current_time = str(datetime.utcnow()).split(".")
            # result.append([EVT_1[i],TMPtimeEVT_1,None,current_time[0]])
            result.append([EVT_1[i],TMPtimeEVT_1])
    return result

def get_event_logs(query:str) -> list:
    c = wmi.WMI()
    # Query the Win32_NTLogEvent class for events with the specified Event ID
    events = c.query(query)
    return [event in events]

def LoginCombine(LoginEvts,LogOffEvts):
    result = []
    for login in LoginEvts:
        for logoff in LogOffEvts:
            loginData = getData(login.Message)
            logoffData = getData(logoff.Message)
            if loginData["Logon ID"] == logoffData["Logon ID"] and loginData["Security ID"] == logoffData["Security ID"]:
                # result.append([loginData,TimeFormat(login.TimeGenerated),logoffData,TimeFormat(logoff.TimeGenerated)])
                result += [loginData,TimeFormat(login.TimeGenerated)]
    return result

def CreateTimeLine(BootTimeLine,LoginTimeLine,ProcessTimeLine):
    Timeline = []
    tmp = []

    for Boot in BootTimeLine:
        Timeline.append([Boot[1],"Boot"]) # Append the start time and Type of the evt
        for login in LoginTimeLine:
            # check that the start time of login is greater than the boot start time
            Boot_time = datetime.strptime(Boot[1], '%Y-%m-%d %H:%M:%S')
            LogIn_time = datetime.strptime(login[1], '%Y-%m-%d %H:%M:%S')

            if LogIn_time > Boot_time and LogIn_time not in tmp:
                # Append the start and end time , user and Type of the evt
                Timeline.append([login[1],"Login",login[0]["Account Name"]])
                tmp.append(LogIn_time)
                for Process in ProcessTimeLine:
                    Process_time = datetime.strptime(Process[1], '%Y-%m-%d %H:%M:%S')
                    if Process_time > LogIn_time and Process_time not in tmp:
                        try:
                            Timeline.append([Process[1],"Process Creation",Process[0]["New Process Name"],Process[0]["Process Command Line"]])
                        except:
                            Timeline.append([Process[1],"Process Creation",Process[0]["New Process Name"]])
                        tmp.append(Process_time)
    return Timeline
        
def PrintTimeLine(TimeLine):
    print(Style.RESET_ALL)
    for each in TimeLine:
        output = ""
        Mal = ""
        hash = ""
        color = ""
        if "Login" in each:
            count = 2
            output = Style.RESET_ALL + " ".join(each[2:])

        elif "Process Creation" in each:
            if "KeyLogger" in each[2]: pass
            count = 4
            output = " ".join(each[2:]) 
            hash = str(SHA256_Hash(each[2]))
            color = Fore.RED if yara_detection(each[2]) else Style.RESET_ALL
        print(f"[{each[0]}]",end=" ")
        print(Style.RESET_ALL+count*' ',each[1],end=" ")
        if len(each) > 2:
            print(color+output,end=" ")
            print(Fore.BLUE+hash,end=" ")
            print(Fore.RED+Mal)
        print(Style.RESET_ALL)

def SHA256_Hash(process_path):
    Size = 65536  # lets read stuff in 64kb chunks!
    sha256 = hashlib.sha256()
    try:
        with open(process_path, 'rb') as f:
            while True:
                data = f.read(Size)
                if not data: break
                sha256.update(data)
    except: return ""
    return sha256.hexdigest()

def getData(msg):
    data = {}
    msg = msg.split('\r\n')
    for value in msg:
        value = value.strip('\t').split(':')
        try:
            if "New Process Name" == value[0] or "Process Command Line" == value[0]:
                data[value[0]] = value[1].strip("\t")+":"+value[2]
            else: data[value[0]] = value[1].strip("\t")
        except IndexError: pass
    return data
                
def GetBoot():
    evt_27 = get_event_logs(f"SELECT * FROM Win32_NTLogEvent WHERE EventCode = 27")
    evt_1074 = get_event_logs(f"SELECT * FROM Win32_NTLogEvent WHERE EventCode = 1074")
    BootTimeLine = Combine(evt_27,evt_1074)
    return BootTimeLine

def GetLogIn():
    evt_4624 = get_event_logs(f"SELECT * FROM Win32_NTLogEvent WHERE EventCode = 4624")
    evt_4647 = get_event_logs(f"SELECT * FROM Win32_NTLogEvent WHERE EventCode = 4647")

    FilterdEvt4624 = []
    for event in evt_4624:
        data = getData(event.Message)
        if data["Security ID"].startswith("S-1-5-21"): FilterdEvt4624 += event
    
    FilterdEvt4647 = []
    for event in evt_4647:
        data = getData(event.Message)
        if data["Security ID"].startswith("S-1-5-21"): FilterdEvt4647 += event
    LoginTimeLine = LoginCombine(FilterdEvt4624,FilterdEvt4647)
    return LoginTimeLine

def GetProcess():
    evt_4688 = get_event_logs(f"SELECT * FROM Win32_NTLogEvent WHERE EventCode = 4688")
    Timeline = []
    for event in evt_4688:
        data = getData(event.Message)
        Timeline.append([data,TimeFormat(event.TimeGenerated)])
    return Timeline


if __name__ == "__main__":
    try:
        banner()
        Boot = GetBoot()
        Login = GetLogIn()
        process = GetProcess()
        Timeline = CreateTimeLine(Boot,Login,process)
        PrintTimeLine(Timeline)
    except KeyboardInterrupt:
        print("Canceled")
