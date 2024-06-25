#!/user/bin/python3
import collector
from sys import argv, stderr
from system import windows
from interface import LogEntry

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
        evt_logs = {
            "security": load_security_records(),
            #"system": load_system_records()
        }
        print("Security Records:", len(evt_logs["security"]))
        #print("System Records:", len(evt_logs["system"]))
        
        # Optionally, print a sample record to check parsing
        if evt_logs["security"]:
            print("Sample Security Record:", LogEntry(evt_logs["security"][0]) )
        # if evt_logs["system"]: print("Sample System Record:", evt_logs["system"][0])
    except KeyboardInterrupt:
        print("[i] aborted by user", file=stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=stderr)
