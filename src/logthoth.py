#!/usr/bin/python3
from logthoth import *

if __name__ == '__main__':
    import time
    from sys import argv, stderr
    start_time = time.time()                        # run time marking
    try:
        evtlogs = {}
        
        collection_start_time = time.time()         # run time marking
        print("(~) collection phase...", end='\r')
        try: evtlogs["security"] = load_security_records(argv[1])
        except IndexError: evtlogs["security"] = load_security_records()
        collection_end_time = time.time()           # run time marking
        print("(i) collected security records:", len(evtlogs["security"]))
        
        parse_start_time = time.time()              # run time marking
        print("(~) parsing phase...", end='\r')
        evtlogs["security"] = [classify(i) for i in evtlogs["security"]]
        print("(i) parsing phase...done") 
        parse_end_time = time.time()                # run time marking
       

        scope_start_time = time.time()
        print("(~) timeline creation phase...", end='\r')
        supertimeline = timeline.activity.scope(name='super timeline', events=evtlogs["security"])
        print("(i) timeline creation...done") 
        scope_end_time = time.time()
        
        # print a sample record to check parsing
        fetch_start_time = time.time()              # run time marking

        print("(~) output json...", end='\r')
        try: timeline_json_dump(supertimeline)
        except (KeyError, IndexError): pass
        print("(i) output json...done") 
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
    scoping_time = scope_end_time - scope_start_time 

    # Print the timings
    print(f"Collection time:      {collection_time:.2f} seconds")
    print(f"Parsing time:         {parsing_time:.2f} seconds")
    print(f"Scoping time:         {scoping_time:.2f} seconds")
    print(f"Fetching sample time: {fetching_time:.2f} seconds")
    print(f"Total execution time: {total_elapsed_time: .2f} seconds")
