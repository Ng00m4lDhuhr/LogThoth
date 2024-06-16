from Evtx.Evtx import Evtx
from sys import argv, stderr
from system import windows


class IntegrityError(Exception):
    """
    class to handls log files integrity errors
    """
    pass


def load_records(filepath: str, ignoreIntegrity: bool = False) -> list:
    # TODO  validate with os.path module https://www.geeksforgeeks.org/os-path-module-python/
    #       check if it's legit path
    #       check if it's a file path
    with Evtx(filepath) as evtx:
        # TODO  warn user if logs are not authenticated
        #       evtx.get_file_header()
        #       if evtx._fh.is_dirty() or not evtx._fh.verify(): raise IntegrityError("Log file has been manipulated")
        return [ record.lxml() for record in evtx.records() ]


# driver/testing code
if __name__ == '__main__':
    try: logsource = argv[1]
    except IndexError: logsource = windows.default.SecurityLogFilePath
    try:
        evtlogs = load_records(filepath=logsource,ignoreIntegrity=False)
        print(evtlogs[1].find("./System/EventID")) # parsing attempts
    except KeyboardInterrupt:
        print("[i] aborted by user")
