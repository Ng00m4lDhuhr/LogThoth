from LogThoth.Activity import *
from LogThoth.Timeline import *
from LogThoth.UI import *

# Query the Win32_NTLogEvent class for events with the specified Event ID
               
BOOT_QUERY = "SELECT * FROM Win32_NTLogEvent WHERE EventCode = 27"
SHUTDOWN_QUERY = "SELECT * FROM Win32_NTLogEvent WHERE EventCode = 1074"
LOGIN_QUERY = "SELECT * FROM Win32_NTLogEvent WHERE EventCode = 4624"
LOGOFF_QUERY = "SELECT * FROM Win32_NTLogEvent WHERE EventCode = 4647"
PROCESS_CREATION_QUERY = "SELECT * FROM Win32_NTLogEvent WHERE EventCode = 4688"

# TODO USER_SID = "S-1-5-21"
NT_AUTHORITY_SID = "S-1-5"
NT_SERVICE_SID = "S-5-80"
NORMAL_USER_SID = "S-1-5-21"
SERVICES_SID = "S-1-5-80-0"

