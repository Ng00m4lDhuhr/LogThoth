"""
Each event log has enough info to understand the context of the record
This code should provide a container that encompasses all the logs within a defined context
"""

from interface import log
from timeline import context as id

class scope(object):
    """abstract/virtual container class of events within a specific context"""

    _counter = 0

    def __init__(self, name:str=None,  events:list=None) -> None:
        
        # TODO  add an incremental id for each scope created 
        #       name the scope f"activity #{self.id}" 
        #       if a name was given do not increase counter
        
        if name == None: 
            self.name = f"Activity #{scope._counter}"
            scope._counter += 1
        else : self.name = name

        # prelisted events case
        if type(events) is list:
            for i in events:
                if not( type(i) is log.event or type(i) is self.__class__): 
                    raise ValueError(f"List should only contain interface.log.event class objects. found {type(i)}")
            events.sort()
        # empty scope case
        else: self.event : list = events or []

    
    def empty(self) -> bool:
        if len(self.event) > 0: return False
        return True

    @property
    def initial(self):
        """The initial property."""
        return self.event[0]
    
    @property
    def final(self):
        """The initial property."""
        return self.event[-1]

    # Making scope sortable based on the initial event time
    def __gt__(self, other:object) -> bool:
        if self.empty(): True # to the infinity and beyond
        return self.initial > other.initial
    
    def __lt__(self, other:object) -> bool:
        if self.empty(): False # to the infinity and beyond
        return self.initial < other.initial
    
    def __ge__(self, other:object) -> bool:
        if self.empty(): True # to the infinity and beyond
        return self.initial >= other.initial
    
    def __le__(self, other:object) -> bool:
        if self.empty(): False # to the infinity and beyond
        return self.initial <= other.initial
    
    def before(self, other:object) -> bool:
        if self.empty() or other.empty : raise TypeError("cannot compare empty scopes")
        return self.final <= other.initial

    def after(self, other:object) -> bool:
        if self.empty() or other.empty : raise TypeError("cannot compare empty scopes")
        return self.initial >= self.final

    def within(self, other:object) -> bool:
        if self.empty() or other.empty : raise TypeError("cannot compare empty scopes")
        return (self > other) and (self.final > other.final)
 
    def encompass(self, other:object) -> bool:
        return (self < other) and (self.final > other.final)

    def checkcontext(self, event:log.event) -> bool: return True

    def insert(self, event:log.event) -> bool:
        if not self.checkcontext(event): return False
        self.event.append(event)
        self.event.sort() # utilize the built-in algorithm called Timsort. 
        return True


class session(scope):
    """class of a logon session context"""
    
    def __init__(self, context:id.session, name:str=None, events:list=None) -> None:
        self.context = context
        if name == None: 
            name = f" User {context.username}@{context.host} Session"
        super().__init__(name=name, events=events)

    def checkcontext(self, event:log.event) -> bool:
        # TODO assert by SID, computer, LogonID
        return (
            self.context.sid  == event.sid and
            self.context.host == event.computer and
            self.context.lid == event.lid
        )
    
    def insert(self, event:log.event) -> bool:
        # first element must be a successful login
        if self.empty(): 
            try: assert event.is_logon() and event.is_successful()
            except AssertionError: return False
        
        # if last element is a logoff prevent insertion
        elif self.final.is_logoff(): return False
        
        return super(session, self).insert(event)

