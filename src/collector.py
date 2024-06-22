from Evtx.Evtx import Evtx
import os
from lxml import etree

class IntegrityError(Exception):
    """
    class to handls log files integrity errors
    """
    pass

def validate_file_path(filepath: str) -> bool:
    """
    class to validate if the provided path is a legitimate file path.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} does not exist.")
    if not os.path.isfile(filepath):
        raise ValueError(f"The path {filepath} is not a file.")
    return True

def load_file_records(filepath: str, ignoreIntegrity: bool = False) -> list:
    validate_file_path(filepath)

    with Evtx(filepath) as evtx:
        # TODO  warn user about logs integrity
        if not ignoreIntegrity:
            evtx.get_file_header()
            if evtx._fh.is_dirty() or not evtx._fh.verify():
                raise IntegrityError("Log file has been manipulated")
        return [ record.lxml() for record in evtx.records() ]

# Defining namespace to handle parsing processs
ns = {"e": "http://schemas.microsoft.com/win/2004/08/events/event"}

def parse_log_record(record) -> dict:
    """Parse an EVTX log record and return a dictionary of its contents."""
    event_data = {}
    
    try:
        event_data["EventID"] = record.find(".//e:EventID", namespaces=ns).text
        event_data["TimeCreated"] = record.find(".//e:TimeCreated", namespaces=ns).get("SystemTime")
        event_data["Computer"] = record.find(".//e:Computer", namespaces=ns).text
        event_data["Channel"] = record.find(".//e:Channel", namespaces=ns).text
        
        data_elements = record.findall(".//e:Data", namespaces=ns)
        for data in data_elements:
            event_data[data.get("Name")] = data.text
    except Exception as e:
        print(f"Error parsing record: {e}")
    
    return event_data

# driver/testing code
if __name__ == '__main__':
    from sys import argv, stderr
    from system import windows
    from windows import DefaultPaths
    
    try:
        log_source = argv[1] if len(argv) > 1 else DefaultPaths.SECURITY_LOG_FILE_PATH
        evt_logs = load_file_records(filepath=log_source, ignore_integrity=True)
        parsed_logs = [parse_log_record(log) for log in evt_logs]
        print(parsed_logs[0])  # Display first parsed log for testing
    except KeyboardInterrupt:
        print("(i) aborted by user", file=stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=stderr)
