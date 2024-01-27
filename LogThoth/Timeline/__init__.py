# Module should take a list of logs and form a timeline of the logs
# It should be able to return an interactive timeline that is mutable
# Said time line can be export in different formats for preservation
# https://dadoverflow.com/2021/08/17/making-timelines-with-python/

import LogThoth.Timeline.Activity
import LogThoth.Timeline.Event

class Timeline(object):
    # class that should represent a timeline
    # it contain an time ordered list of Event objects
    def __init__(self, EventList:list) -> None:
        pass


if __name__ == '__main__':
    # lol there is nothing to do
    pass
