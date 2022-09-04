class EventRequest:
    
    def __init__(self, EventType, RetryCount):
        self.EventType = "R"
        self.RetryCount = RetryCount
    
    def __str__(self):
        return f"EventRequest: {self.EventType}, {self.RetryCount}"

class EventStatus:
    
    def __init__(self, EventType, StatusType, RetryCount):
        self.EventType = "S"
        self.StatusType = StatusType
        self.RetryCount = RetryCount
    
    def __str__(self):
        return f"EventStatus: {self.EventType}, {self.StatusType}, {self.RetryCount}"
    
input_queue = [['S', 'P', 0], ['R', 0], ['S', 'M', 0], ['S', 'P', 0], ['S', 'T', 0], ['S', 'P', 0], ['S', 'C', 0], ['S', 'M', 0]]
queue = []
event_lookup = []

def push(EventType = "", RetryCount = 0, StatusType = None):
    if EventType == "S":
        queue.append(EventStatus(EventType, StatusType, RetryCount))
    if EventType == "R":
        queue.append(EventRequest(EventType, RetryCount))
    return {
        "success": True,
        "error": False,
        "msg": "Executed!"
    }


def pop():
    while queue:
        obj = queue.pop(0)
        if obj.EventType == "S":
            print(obj)
            if obj.StatusType in ['C', 'T'] and obj.RetryCount < 2:
                obj.RetryCount += 1
                push(obj.EventType, obj.RetryCount, obj.StatusType)
        else:
            last_object = event_lookup.pop() if len(event_lookup) > 0 else None
            if last_object and last_object[0] == 'S' and last_object[1] in ['C', 'T']:
                print(obj)
            else:
                obj.RetryCount += 1
                push(obj.EventType, RetryCount = obj.RetryCount)
        event_lookup.append([obj.EventType, obj.RetryCount, obj.StatusType if obj.EventType == 'S' else ''])
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
        if data[1] not in ['P', 'M', 'C', 'T']:
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
    if not data or data[0] not in ["S", "R"] or (data[0] == "S" and not len(data) == 3) or (data[0] == "R" and not len(data) == 2):
        msg = "All values are not Specified!"
        return {
            "success": False,
            "error": True,
            "msg": msg
        }
    
    response = vaildate_data(data)
    if response['error']:
        return response['msg']
    
    EventType = data[0]
    StatusType = data[1] if EventType == "S" else ""
    RetryCount = data[1] if EventType == "R" else data[2]
    push(EventType, RetryCount, StatusType)
    return {
        "success": True,
        "error": False,
        "msg": "Executed!"
    }
    
def intialization():
    for data in input_queue:
        format_data(data)
    pop()

intialization()
