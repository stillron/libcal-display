class Event:
    
    def __init__(self):
        
        self.title = None
        self.start_time = None
        self.end_time = None
        self.weekday = None
        self.month = None
        self.day = None
        self.campus = None
        self.location = None
        self.description = None
        self.image = None
        self.rotate_x = None
        self.rotate_y = None
        self.rotate_z = None
        self.scale = None
        self.xcor = None
        self.ycor = None
        self.zcor = None

class EventsManager:
    
    def __init__(self, raw_events=[]):
        self.events = []
        self.raw_events = raw_events
        self.sort_events()
        
    def sort_events(self):
        self.events = sorted( raw_events, key=lambda x: x.get('start'))
        