class EventRequest:
    EventType #’R’ for EventRequest
    RetryCount #E.g. 0, 1, 2, 3, etc.
    
    def __init__(self, EventType, RetryCount):
        self.EventType = "R"
        self.RetryCount = RetryCount
    
    def __str__(self):
        return f"EventRequest: {EventType}, {RetryCount}"

class EventStatus:
    EventType #‘S’ for EventStatus
    StatusType #Can be only one of : ‘P’, ‘M’, ‘C’ or ‘T’
    RetryCount #E.g. 0, 1, 2, 3, etc.
    
    def __init__(self, EventType, StatusType, RetryCount):
        self.EventType = "S"
        self.StatusType = StatusType
        self.RetryCount = RetryCount
    
    def __str__(self):
        return f"EventStatus: {EventType}, {StatusType}, {RetryCount}"
    
queue = []

def push(EventType, StatusType, RetryCount):
    if EventType == "S":
        eventStatus = EventStatus(EventType, StatusType, RetryCount)
    if EventType == "R":
        eventStatus = EventStatus(EventType, RetryCount)
    queue.append(eventStatus)
    return {
        "success": True,
        "error": False,
        "msg": "Executed!"
    }

def pop():
    return {
        "success": True,
        "error": False,
        "msg": "Executed!"
    }

def vaildate_data(data):
    
    success = True
    error = False
    msg = "Executed!"
    
    if data[0] == 'S':
        msg = None
        if data[1] not in [‘P’, ‘M’, ‘C’, ‘T’]:
            msg = "StatusType must be one of these!"
        
        if not isinstance(data[2], int) or data[2] != 0:
            msg = "RetryCount must be 0 and a number!"
            
    if data[0] == 'R':
        
        if not isinstance(data[1], int) or data[1] != 0:
            msg = "RetryCount must be 0 and a number!"
    return {
        "success": success,
        "error": error,
        "msg": msg
    }
        
def format_data(data):
    if not data or data[0] not in ["S", "R"] or (EventType == "S" and not data.len() == 3) or (EventType == "R" and not data.len() == 2):
        msg = "All values are not Specified!"
        return return {
            "success": False,
            "error": True,
            "msg": msg
        }
    
    response = vaildate_data(data)
    if response['error']:
        return response['msg']
    
    EventType = data[0]
    StatusType = data[1] if EventType == "S" else None
    RetryCount = data[1] if EventType == "R" else data[2]
    push(EventType, StatusType, RetryCount)
    return {
        "success": True,
        "error": False,
        "msg": "Executed!"
    }
    
def intialization():
    data = input()
    push(data)
