from Evtx.Evtx import Evtx
import os
from lxml import etree
from interface import log

class IntegrityError(Exception):
    """
    class to handls log files integrity errors
    """
    pass

  
def assert_file_path(filepath: str) -> bool:
    """
    function to assert if the provided path is a legitimate file path.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} does not exist.")
    if not os.path.isfile(filepath):
        raise ValueError(f"The path {filepath} is not a file.")
    return True


def load_file_records(filepath: str, ignoreIntegrity: bool = False) -> list:
    assert_file_path(filepath)
    with Evtx(filepath) as evtx:
        # TODO  warn user about logs integrity
        if not ignoreIntegrity:
            evtx.get_file_header()
            if evtx._fh.is_dirty() or not evtx._fh.verify():
                raise IntegrityError("None trusted log source")
        return [ record.lxml() for record in evtx.records() ]


# driver/testing code
if __name__ == '__main__':
    from sys import argv, stderr
    from system import windows

    try:
        log_source = argv[1] if len(argv) > 1 else windows.default.path['SecurityLogFile'] 
        evt_logs = load_file_records(filepath=log_source, ignoreIntegrity=True)
        parsed_logs = [log.event(log) for log in evt_logs]
        print(parsed_logs[0])  # Display first parsed log for testing

    except KeyboardInterrupt:
        print("(i) aborted by user", file=stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=stderr)
