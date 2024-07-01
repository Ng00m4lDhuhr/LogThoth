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
    filepath = filepath or windows.default.path['SecurityLogFile']
    return collector.load_file_records(filepath=filepath,ignoreIntegrity=True)

def load_system_records   (filepath:str=None) -> list:
    filepath = filepath or windows.default.path['SystemLogFile']
    return collector.load_file_records(filepath=filepath,ignoreIntegrity=True)


def classify(record:object) -> log.event:
    """ function that decides the type of a log entry """
    event_id = int(record.find(".//e:EventID", namespaces=log.event.ns).text)

    if   event_id == 4624: return log.evt4624(record)
    elif event_id == 4625: return log.evt4625(record)
    elif event_id == 4634: return log.evt4634(record)
    elif event_id == 4647: return log.evt4647(record)
    elif event_id == 4688: return log.evt4688(record)
    elif event_id == 4689: return log.evt4689(record)
    else: return log.event(record) #idk idc

if __name__ == '__main__':

    start_time = time.time()                        # run time marking
    try:
        evtlogs = {}
        
        collection_start_time = time.time()         # run time marking
        print("(~) collection phase...", end='\r')
        evtlogs["security"] = load_security_records()
        collection_end_time = time.time()           # run time marking
        print("(i) collected security records:", len(evtlogs["security"]))
        
        parse_start_time = time.time()              # run time marking
        print("(~) parsing phase...", end='\r')
        for i in evtlogs["security"]: i = classify(i)
        print("(i) parsing phase...done") 
        parse_end_time = time.time()                # run time marking
        
        # print a sample record to check parsing
        fetch_start_time = time.time()           # run time marking
        try:
            if evtlogs["security"]:
                print("Sample Security Record:", evtlogs["security"][0])
        except (KeyError, IndexError): pass
        fetch_end_time = time.time()                # run time marking
      

    except KeyboardInterrupt:
        print("(i) aborted by user", file=stderr)
        quit()
    end_time = time.time()                          # run time marking
    
    # Calculate elapsed times
    total_elapsed_time = end_time - start_time
    collection_time = collection_end_time - collection_start_time
    parsing_time = parse_end_time - parse_start_time
    fetching_time = fetch_end_time - fetch_start_time

    # Print the timings
    print(f"Collection time:      {collection_time:.2f} seconds")
    print(f"Parsing time:         {parsing_time:.2f} seconds")
    print(f"Fetching sample time: {fetching_time:.2f} seconds")
    print(f"Total execution time: {total_elapsed_time: .2f} seconds")
