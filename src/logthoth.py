#!/usr/bin/python3
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
        collection_start_time = time.time()
        print("(~) collection phase...", end='\r')
        try:
            evtlogs["security"] = load_security_records()
            print("(i) collected security records:", len(evtlogs["security"]))

        except Exception as e:
            print("(!) cannot collect security file:",e, file=stderr)
          
        try:
            evtlogs["system"] = load_system_records()
            print("System Records:", len(evtlogs["system"]) )
        except Exception as e:
            print("(!) cannot collect system file:",e, file=stderr)
        collection_end_time = time.time()

        parsing_start_time = time.time()
        print("(~) parsing phase...", end='\r')
        try:
            for event in evtlogs["security"]: event = log.classify(event)
            print("(i) parsing phase...done") 
        except Exception as e:
            print("(!) cannot parse security logs:", e, file=stderr)
        parse_end_time = time.time()
      
        # print a sample record to check parsing
        fetching_start_time = time.time()
        try:
            if evtlogs["security"]:
                print("Sample Security Record:", evtlogs["security"][0])
        except (KeyError, IndexError): pass
        
        try:
            if evtlogs["system"]:
                print("Sample Security Record:", evtlogs["system"][0])
        except (KeyError, IndexError): pass
        fetch_end_time = time.time() 
      
    except KeyboardInterrupt:
        print("(i) aborted by user", file=stderr)
        quit()
    end_time = time.time() # End the timer
    
    # Calculate elapsed times
    total_elapsed_time = end_time - start_time
    collection_time = collection_end_time - collection_start_time
    parsing_time = parsing_end_time - parsing_start_time
    fetching_time = fetching_end_time - fetching_start_time

    # Print the timings
    print(f"Collection time:      {collection_time:.2f} seconds")
    print(f"Parsing time:         {parsing_time:.2f} seconds")
    print(f"Fetching sample time: {fetching_time:.2f} seconds")
    print(f"Total execution time: {total_elapsed_time: .2f} seconds")
