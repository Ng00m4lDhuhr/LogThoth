#!/user/bin/python3
import collector
from sys import argv, stderr
from system import windows
from windows import DefaultPaths

def load_security_records (filepath:str=None) -> list:
    filepath = filepath or DefaultPaths.SECURITY_LOG_FILE_PATH
    evt_logs = collector.load_file_records(filepath=filepath, ignore_integrity=True)
    return [collector.parse_log_record(log) for log in evt_logs]

def load_system_records   (filepath:str=None) -> list:
    filepath = filepath or DefaultPaths.SYSTEM_LOG_FILE_PATH
    evt_logs = collector.load_file_records(filepath=filepath, ignore_integrity=True)
    return [collector.parse_log_record(log) for log in evt_logs]


if __name__ == '__main__':
    try:
        evt_logs = {
            "security": load_security_records(),
            "system": load_system_records()
        }
        print("Security Records:", len(evt_logs["security"]))
        print("System Records:", len(evt_logs["system"]))
        # Optionally, print a sample record to check parsing
        if evt_logs["security"]:
            print("Sample Security Record:", evt_logs["security"][0])
        if evt_logs["system"]:
            print("Sample System Record:", evt_logs["system"][0])
    except KeyboardInterrupt:
        print("[i] aborted by user", file=stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=stderr)
