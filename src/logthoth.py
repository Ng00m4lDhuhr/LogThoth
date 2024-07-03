#!/usr/bin/python3
import collector
from sys import argv, stderr
from interface.system import windows
from interface import log
import timeline


class CollectionError(Exception):
  """class to signal log file reading errors"""

class ParsingError(Exception):
  """class to signal log file parsing errors"""

class ContextError(Exception):
  """class to signal context scope errors"""
  
  
def load_security_records (filepath:str=None) -> list:
    filepath = filepath or windows.default.path['SecurityLogFile']
    return collector.load_file_records(filepath=filepath,ignoreIntegrity=True)

def load_system_records   (filepath:str=None) -> list:
    filepath = filepath or windows.default.path['SystemLogFile']
    return collector.load_file_records(filepath=filepath,ignoreIntegrity=True)


def classify(record:object) -> log.event:
    """ function that decides the type of a log entry """
    event_id = int(record.find(".//e:EventID", namespaces=log.event.ns).text)

    event_handlers = {
        4624: log.evt4624,
        4625: log.evt4625,
        4634: log.evt4634,
        4647: log.evt4647,
        4688: log.evt4688,
        4689: log.evt4689,
    }
    # Return the appropriate log event handler based on event_id,
    # or default to log.event if event_id is not recognized.
    return event_handlers.get(event_id, lambda r: log.event(r))(record)

if __name__ == '__main__':
    import time
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
        evtlogs["security"] = [classify(i) for i in evtlogs["security"]]
        print("(i) parsing phase...done") 
        parse_end_time = time.time()                # run time marking
        
        # print a sample record to check parsing
        fetch_start_time = time.time()              # run time marking
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
