"""
The purpose of this code is to define default windows values
and to query said values if have been simply changed
"""

from sys import argv, stderr
from os import environ, path


# class instance to hold default pathes need for acqusition
class default(object):
    SystemRoot : str = "C:\\Windows"
    LogFolderPath : str = SystemRoot + "\\system32\\winevt\\Logs"
    SystemLogFilePath : str = LogFolderPath + "\\System.evtx"
    SecurityLogFilePath : str = LogFolderPath + "\\Security.evtx"

# static class to query live environment
class query(object):

    @staticmethod
    def SystemRoot() -> str: return environ['SystemRoot']

    @staticmethod
    def HostName() -> str: return environ['COMPUTERNAME']
    # TODO query each evtx file path from registry key "\\HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\EventLog\\"
