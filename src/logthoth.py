#!/user/bin/python3
import collector
from sys import argv, stderr
from interface.system import windows
from interface import log

def load_security_records (filepath:str=None) -> list:
    # default path or given file path
    filepath = filepath or windows.default.path['SecurityLogFile']
    return collector.load_file_records(filepath=filepath,ignoreIntegrity=True)

def load_system_records   (filepath:str=None) -> list:
    # default path or given file path
    filepath = filepath or windows.default.path['SystemLogFile']
    return collector.load_file_records(filepath=filepath,ignoreIntegrity=True)


if __name__ == '__main__':
    try:
        print("(~) collection phase...", end='\r')
        evt_logs = {
            "security": load_security_records(),
            #"system": load_system_records()
        }
        print("(i) collected security records:", len(evt_logs["security"]))
        #print("System Records:", len(evt_logs["system"]))
        print("(~) parsing phase...", end='\r')
        for event in evt_logs["security"]:
            event = log.classify(event)
        # Optionally, print a sample record to check parsing
        if evt_logs["security"]:
            print("Sample Security Record:", log.event(evt_logs["security"][0]) )
        # if evt_logs["system"]: print("Sample System Record:", evt_logs["system"][0])
    except KeyboardInterrupt:
        print("[i] aborted by user", file=stderr)
