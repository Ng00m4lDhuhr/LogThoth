#!/user/bin/python3
import collector
from sys import argv, stderr
from interface.system import windows
from interface import log
import time

class CollectionError(Exception):
  """class to signal log file reading errors"""

class ParsingError(Exception):
  """class to signal log file parsing errors"""
  
  
def load_security_records (filepath:str=None) -> list:
    # default path or given file path
    filepath = filepath or windows.default.path['SecurityLogFile']
    return collector.load_file_records(filepath=filepath,ignoreIntegrity=True)

def load_system_records   (filepath:str=None) -> list:
    # default path or given file path
    filepath = filepath or windows.default.path['SystemLogFile']
    return collector.load_file_records(filepath=filepath,ignoreIntegrity=True)


if __name__ == '__main__':
  start_time = time.time() #Start the timer
    try:
        evtlogs = {}
        
        print("(~) collection phase...", end='\r')
        try:
          evtlogs["security"] = load_security_records()
          print("(i) collected security records:", len(evt_logs["security"]))
        except Exception as e:
          print("(!) cannot parse security file:",e, file=stderr)
          
        try:
          evtlogs["system"] = load_system_records()
          print("System Records:", len(evtlogs["system"]) )
        except Exception as e:
          print("(!) cannot parse system file:",e, file=stderr)
          
        print("(~) parsing phase...", end='\r')
        try:
          for event in evt_logs["security"]: event = log.classify(event)
        print("(i) parsing phase...done") 
        except Exception as e:
          print("(!) cannot parse security logs:", e, file=stderr)
        
        # print a sample record to check parsing
        try:
          if evtlogs["security"]:
            print("Sample Security Record:", evt_logs["security"][0])
        except KeyError: pass
        except IndexError: pass
     
        try:
          if evtlogs["system"]:
            print("Sample Security Record:", evt_logs["system"][0])
        except KeyError: pass
        except IndexError: pass
        
    except KeyboardInterrupt:
        print("[i] aborted by user", file=stderr)
        quit()
end_time = time.time() # End the timer
elapsed_time = end_time - start_time # Calculate elapsed time
print(f"Total execution time: {elapsed_time: .2f} seconds")
