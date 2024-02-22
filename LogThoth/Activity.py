from datetime import datetime, timezone

class Activity(object):
    def __init__(self, log: object) -> None:
        self.rawlog = log
        self.time =  self.ParseTime(log.TimeGenerated)
        self._data = None

    @property
    def data(self):
        # memorization of data
        # only parsed if needed
        if self._data == None: self.GetData()
        return self._data


    def __lt__(self, other:object): return self.time < other.time
    def __gt__(self, other:object): return self.time > other.time

    def __eq__(self, other:object):
        return self.rawlog.RecordNumber == other.rawlog.RecordNumber

    def __hash__(self): return int(self.rawlog.RecordNumber)

    # state changing function that changes object 
    # but return nothing as it meant to be internal
    def GetData(self) -> None:
        self._data = self.ParseData(self.rawlog.Message)
        # add your custom parsing here

    # parses the data string from wmi.WMI().query(SELECT * FROM Win32_NTLogEvent)[0].Message
    # it looks like this
    """
    Category         : 33
    CategoryString   :
    EventCode        : 27
    EventIdentifier  : 27
    TypeEvent        :
    InsertionStrings : {0,  NOEXECUTE=OPTIN  HYPERVISORLAUNCHTYPE=AUTO  FVEBOOT=2674688  NOVGA}
    LogFile          : System
    Message          : The boot type was 0x0.
    RecordNumber     : 134133
    SourceName       : Microsoft-Windows-Kernel-Boot
    TimeGenerated    : 20240131103252.892359-000
    TimeWritten      : 20240131103252.892359-000
    Type             : Information
    UserName         :
    """
    
    @staticmethod
    def ParseData(rawdata:str) -> dict:
        data = {}
        # split it into list of lines
        rawdata = rawdata.strip('\t').split('\r\n')
        for line in rawdata:
            line = line.strip('\t').split(':')
            try: 
                data[line[0]] = line[1].strip('\t')
            except IndexError: pass  # EHE TE NANDAYOO >_<
        return data
    
    @staticmethod
    def ParseTime(rawtime:str) -> datetime:
        year        = rawtime [  : 4]
        month       = rawtime [ 4: 6]
        day         = rawtime [ 6: 8]
        hour        = rawtime [ 8:10]
        minute      = rawtime [10:12]
        second      = rawtime [12:14]
        microsecond = rawtime [15:21]
        zone        = rawtime [22:  ]

        return datetime(year        = int(year),        month       = int(month),
                        day         = int(day),         hour        = int(hour),
                        minute      = int(minute),      second      = int(second),
                        microsecond = int(microsecond), tzinfo      = timezone.utc
                        )


# ONLY FOR TESTING
if __name__ == '__main__':
    # test time parser
    raw = '20240131103252.892359-000'
    code = Activity.ParseTime(raw)
    print(code)

    # test data parser
    raw = "Creator Subject:\r\n\tSecurity ID:\t\tS-1-5-18\r\n\tAccount Name:\t\t-\r\nAccount Domain:\t\t-\r\n\tLogon ID:\t\t0x3E7\r\n\r\n\r\nTarget Subject:\r\n\tSecurity ID:\t\tS-1-0-0\r\n\tAccount Name:\t\t-\r\n\tAccount Domain:\t\t-\r\n\tLogon ID:\t\t0x0\r\n\r\nProcess Information:\r\n\tNew Process ID:\t\t0x8c\r\n\tNew Process Name:\r\n\tToken Elevation Type:\tTokenElevationTypeDefault (1)\r\n\tMandatory Label:\t\tS-1-16-16384\r\n\tCreator Process ID:\t\t0x4\r\n\tCreator Process Name:\r\n\tProcess Command Line:\r\n"
    code = Activity.ParseData(raw)
    print(code)
