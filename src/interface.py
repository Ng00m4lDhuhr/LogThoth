"""
an interface to easily access xml data as if it was fully deserialized in a data structure
"""

class LogEntry(object):

    """ a class that acts as an interface to the etree of evtlogs records """

    ns = {"e": "http://schemas.microsoft.com/win/2004/08/events/event"}

    def __init__(self, record:object):
        self._record : xmltree = record
        self._data : dict = {}

    def __str__(self) -> str:
        return f"<{self.EventID}/{self.Computer}/{self.Channel}>"
    # Event Record Property

    @property
    def EventID(self) -> int:
        """The EventID property."""
        return int(self._record.find(".//e:EventID", namespaces=self.ns).text)
    
    @property
    def TimeCreated(self):
        """The TimeCreated property."""
        # TODO choose 1 time structure and stick to it
        return self._record.find(".//e:TimeCreated", namespaces=self.ns).get("SystemTime")

    @property
    def Computer(self):
        """The Computer property."""
        return self._record.find(".//e:Computer", namespaces=self.ns).text

    @property
    def Channel(self):
        """The Channel property."""
        return self._record.find(".//e:Channel", namespaces=self.ns).text

    def data(self, ValueName:str) -> object:
        try: return self._data[str(ValueName)]
        except KeyError:
            data_elements = record.findall(".//e:Data", namespaces=self.ns)
            for data in data_elements:
                self._data[data.get("Name")] = data.text
        try: return self._data[str(ValueName)]
        except KeyError: return None



# driver/testing code
if __name__ == '__main__':
    from sys import argv, stderr
    from system import windows
    from collector import load_file_records
    
    try:
        log_source = argv[1] if len(argv) > 1 else windows.default.path['SecurityLogFile'] 
        evt_logs = load_file_records(filepath=log_source, ignoreIntegrity=True)
        parsed_logs = [LogEntry(log) for log in evt_logs]
        print(parsed_logs[0])  # Display first parsed log for testing
    except KeyboardInterrupt:
        print("(i) aborted by user", file=stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=stderr)

