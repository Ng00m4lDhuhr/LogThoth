from Evtx.Evtx import Evtx
from sys import argv, stderr
from system import windows


class IntegrityError(Exception):
    """
    class to handls log files integrity errors
    """
    pass


if __name__ == '__main__':
    try: argv[1]
    except IndexError:
        print("SYNTAX ERROR: no logs file path was given",file=stderr)
        exit()
    with Evtx(windows.default.SecurityLogFilePath) as evtx:
        # TODO warn user if logs are not authenticated
        # evtx.get_file_header()
        # if evtx._fh.is_dirty() or not evtx._fh.verify(): raise IntegrityError("Log file has been manipulated")
        records = [ record.lxml() for record in evtx.records() ]
    print(records[-1])
