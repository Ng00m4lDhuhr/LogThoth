from Evtx.Evtx import Evtx
from sys import argv, stderr
from os import environ, path

# Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\EventLog\

class default(object):
    try:
        system_root = environ['SystemRoot']
        if not path.isdir(system_root) : raise ValueError
    except KeyError:
        system_root = "C:\\Windows\\"
    try:
        logs_path = system_root + "\\winevt\\Logs\\"
        if not path.isdir(logs_path) : raise ValueError
    except ValueError:
        print("you are gay",file=stderr)

def read_logs_file(file_path : str) -> list:
    with Evtx(file_path) as evtx:
        return [ record for record in evtx.records() ]

if __name__ == '__main__':
    try:
        records = read_logs_file(argv[1])
        print(records[0])
    except IndexError: print("SYNTAX ERROR: no logs file path was given",file=stderr)
