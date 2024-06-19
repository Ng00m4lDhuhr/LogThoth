#!/user/bin/python3
import collector
from sys import argv, stderr
from system import windows

def load_security_records (filepath:str=None) -> list:
    if filepath == None:
        filepath = windows.default.SecurityLogFilePath
    return collector.load_file_records(filepath=filepath,ignoreIntegrity=True)

def load_system_records   (filepath:str=None) -> list:
    if filepath == None:
        filepath = windows.default.SystemLogFilePath
    return collector.load_file_records(filepath=filepath,ignoreIntegrity=True)


if __name__ == '__main__':
    try:
        evtlogs = {}
        evtlogs["security"] = load_security_records()
        evtlogs["system"] = load_system_records()
        print(evtlogs["security"].find("./System/EventID")) # parsing attempts
        print(evtlogs["system"].find("./System/EventID"))   # parsing attempts
    except KeyboardInterrupt:
        print("[i] aborted by user", file=stderr)
        quit()
