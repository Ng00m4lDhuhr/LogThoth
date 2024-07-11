from Evtx.Evtx import Evtx
from os import path


class IntegrityError(Exception):
    """
    class to handls log files integrity errors
    """
    pass


def assert_file_path(filepath: str) -> bool:
    """
    function to assert if the provided path is a legitimate file path.
    """
    if not path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} does not exist.")
    if not path.isfile(filepath):
        raise ValueError(f"The path {filepath} is not a file.")
    return True


def load_file_records(filepath: str, ignoreIntegrity: bool = False) -> list:
    assert_file_path(filepath)
    with Evtx(filepath) as evtx:
        # TODO  warn user about logs integrity
        if not ignoreIntegrity:
            evtx.get_file_header()
            if evtx._fh.is_dirty() or not evtx._fh.verify():
                raise IntegrityError("Untrusted log source")
        return [ record.lxml() for record in evtx.records() ]


