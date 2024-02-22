import wmi

def get_event_logs(query):
    api = wmi.WMI()
    # Query the Win32_NTLogEvent class for events with the specified Event ID
    event_list = [_ for _ in api.query(query)]
    return event_list

if __name__ == '__main__': pass
