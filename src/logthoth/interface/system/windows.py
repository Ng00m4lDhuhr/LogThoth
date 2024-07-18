"""
The purpose of this code is to define default windows values
and to query said values if have been simply changed
"""

from os import environ


# class instance to hold default pathes need for acqusition
class default(object):

    path : dict = {}
    path["SystemRoot"]      = "C:\\Windows"
    path["LogFolder"]       = path["SystemRoot"] + "\\system32\\winevt\\Logs"
    path["SystemLogFile"]   = path["LogFolder"]  + "\\System.evtx"
    path["SecurityLogFile"] = path["LogFolder"]  + "\\Security.evtx"

# translates logon type codes

class logon(object):
    type = {
         2: "local interactive",
         3: "network",
         4: "batch",
         5: "service",
         7: "unlock",
         8: "network clear text",
         9: "new credentials",
        10: "remote interactive",
        11: "cached interactive"
    }
    substatus = {
            # see https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=4625#Failure_Information
            int("0xC0000064", 16): "non-existent username",
            int("0xC000006A", 16): "wrong password",
            int("0xC000006F", 16): "time of day restriction",
            int("0xC0000070", 16): "authentication policy violation",
            int("0xC0000071", 16): "password expired",
            int("0xC0000072", 16): "user disabled",
            int("0xC0000133", 16): "clock out of sync",
            int("0xc000015b", 16): "denied logon type",
            int("0xC0000193", 16): "user expired",
            int("0xC0000224", 16): "password change required",
            int("0xC0000225", 16): "internal windows bug",
            int("0xC0000234", 16): "user locked out"
    }


# static class to query live environment
class query(object):

    @staticmethod
    def systemroot() -> str: return environ['SystemRoot']

    @staticmethod
    def hostname() -> str: return environ['COMPUTERNAME']
    # TODO query each evtx file path from registry key "\\HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\EventLog\\"
