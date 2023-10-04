import datetime as dt
class Event:
    MINUTES_HOURS_FMT = '%-I:%M %p'
    WEEKDAY_FMT = '%A'
    MONTH_FMT = '%B'
    YEAR_FMT = '%Y'
    DAY = "DAY"
    
    def __init__(self, event: dict):
        
        self.id = event.get("id")
        self.title = event.get("title")
        self.start = event.get("start")
        self.end = event.get("end")
        self.start_time = self._get_datetimes(self.start, Event.MINUTES_HOURS_FMT)
        self.end_time = self._get_datetimes(self.end, Event.MINUTES_HOURS_FMT)
        self.weekday = self._get_datetimes(self.start, Event.WEEKDAY_FMT)
        self.year = self._get_datetimes(self.start, Event.YEAR_FMT)
        self.month = self._get_datetimes(self.start, Event.MONTH_FMT)
        self.day = self._get_datetimes(self.start, Event.DAY)
        self.campus = event.get('calendar').get('name').split(" ")[0]
        self.location = event.get('location').get('name')
        self.description = event.get('description')
        self.image = event.get('featured_image')
        self.rotate_x = None
        self.rotate_y = None
        self.rotate_z = None
        self.scale = None
        self.xcor = None
        self.ycor = None
        self.zcor = None

    def _get_datetimes(self, time, fmt):
        """ Takes a string in isoformat and a strftime and returns the part of the string"""

        if time is not None:
            date = dt.datetime.fromisoformat(time)
            if fmt == "DAY":
                return date.day
            else:
                return date.strftime(fmt)
        else:
            return None

    def __repr__(self):
        return f"<Event id#{self.id} {self.title} on {self.start}>"

    def __str__(self):
        return f"{self.title} (id# {self.id}) at {self.campus} on {self.weekday} {self.month} {self.day}, {self.year}"

    def __len__(self):
        """ Returns the duration of the event in minutes """

        start = dt.datetime.fromisoformat(self.start)
        end = dt.datetime.fromisoformat(self.end)
        seconds = int(( end - start).total_seconds())
        return seconds // 60


class EventsManager:
    
    def __init__(self, events=[]):
        self.events = events
        self.sort_events_by_date()
        
    def sort_events_by_date(self):
        self.events.sort(key=lambda x: x.start)

    def add_event(self, event: Event):
        self.events.append(event)
        self.sort_events_by_date()

    def __getitem__(self, position):
        return self.events[position]

    def __len__(self):
        return len(self.events)
        