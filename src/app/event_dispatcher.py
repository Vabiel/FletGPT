class EventDispatcher:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_name:str, handler):
        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        self.subscribers[event_name].append(handler)

    def dispatch(self, event_name:str, data):
        if event_name in self.subscribers:
            for handler in self.subscribers[event_name]:
                handler(data)