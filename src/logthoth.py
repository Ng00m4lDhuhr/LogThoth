#!/usr/bin/python
import collector
from sys import argv, stderr
from system import windows

def load_security_records (filepath:str=None) -> list: pass
def load_system_records   (filepath:str=None) -> list: pass

if __name__ == '__main__':
    try: logsource = argv[1]
    except IndexError: logsource = windows.default.SecurityLogFilePath
    try:
        evtlogs = collector.load_file_records(filepath=logsource,ignoreIntegrity=True)
        print(evtlogs[1].find("./System/EventID")) # parsing attempts
    except KeyboardInterrupt:
        print("[i] aborted by user", file=stderr)
