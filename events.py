class Event:
    
    def __init__(self, title, start_time, end_time, weekday,
                 month, day, campus, location, description=None,
                 image="placeholder.png", rotate_x=None, rotate_y=None,
                 rotate_z=None, scale=None, xcor=None, ycor=None, zcor=None
                 ):
        
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.weekday = weekday
        self.month = month
        self.day = day
        self.campus = campus
        self.location = location
        self.description = description
        self.image = featured_image
        self.rotate_x = rotate_x
        self.rotate_y = rotate_y
        self.rotate_z = rotate_z
        self.scale = scale
        self.xcor = xcor
        self.ycor = ycor
        self.zcor = zcor

class EventsManager:
    
    def __init__(self, raw_events=[]):
        self.events = []
        self.raw_events = raw_events
        self.sort_events()
        
    def sort_events(self):
        self.events = sorted( raw_events, key=lambda x: x.get('start'))
        