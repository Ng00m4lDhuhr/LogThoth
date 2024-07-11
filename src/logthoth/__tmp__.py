#!/usr/bin/python3
from logthoth import collector, timeline
from logthoth.interface.system import windows
from logthoth.interface import log
from json import dump

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

def timeline_json_dump(scope:timeline.activity.scope, file:str='output.json') -> None:
    value = scope.dict()
    with open(file, 'w') as f: 
        dump(value, f, indent=4)
    return None


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


#!/usr/bin/python3
from logthoth import collector, timeline
from logthoth.interface.system import windows
from logthoth.interface import log
from json import dump

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

def timeline_json_dump(scope:timeline.activity.scope, file:str='output.json') -> None:
    value = scope.dict()
    with open(file, 'w') as f: 
        dump(value, f, indent=4)
    return None


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



