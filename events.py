import datetime as dt
import random

class Event:
    MINUTES_HOURS_FMT = '%-I:%M %p'
    WEEKDAY_FMT = '%A'
    MONTH_FMT = '%B'
    YEAR_FMT = '%Y'
    DAY = "DAY"

    events = []
    rotate_x = rotate_y = rotate_z = None
    scale = None
    xcor = ycor = zcor = None

    def __init__(self, event: dict):
        # Event Metadata
        self.id = event.get("id")

        # Event Data
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

        # Impress.js Positional Data
        self.rotate_x = None
        self.rotate_y = None
        self.rotate_z = None
        self.scale = None
        self.xcor = None
        self.ycor = None
        self.zcor = None

    @classmethod
    def sort_events_by_date(cls):
        cls.events.sort(key=lambda x: x.start)

    @classmethod
    def arrange(cls):
        Event.sort_events_by_date()

        arrangements = [
            cls.vertical_chain, cls.horizontal_chain, cls.swoop_around, 
            cls.ring_around, cls.ring_twist, cls.clusters
            ]
        make_arrangement = random.choice(arrangements)
        print(make_arrangement)
        make_arrangement()

    @classmethod
    def vertical_chain(cls):
        cls.xcor = cls.ycor = cls.zcor = cls.rotate_y = 0

        for event in cls.events:
            event.ycor = cls.ycor
            event.rotate_y = cls.rotate_y
            event.xcor = event.zcor = 0
            event.scale = 1
            cls.ycor += 850
            cls.rotate_y += 45

    @classmethod
    def ring_around(cls):
        cls.xcor = cls.ycor = cls.zcor = cls.rotate_z = 0

        for event in cls.events:
            event.ycor = cls.ycor
            event.rotate_z = cls.rotate_z
            event.xcor = event.zcor = 0
            event.scale = 1
            cls.ycor += 1500
            cls.rotate_z += 45

    @classmethod
    def ring_twist(cls):
        cls.xcor = cls.ycor = cls.zcor = cls.rotate_z = cls.rotate_y= 0

        for event in cls.events:
            event.ycor = cls.ycor
            event.rotate_z = cls.rotate_z
            event.rotate_y = cls.rotate_y
            event.xcor = event.zcor = 0
            event.scale = 1
            cls.ycor += 1500
            cls.rotate_z += 45
            cls.rotate_y -= 60

    @classmethod
    def horizontal_chain(cls):
        cls.xcor = cls.ycor = cls.zor = cls.rotate_x = 0

        for event in cls.events:
            event.xcor = cls.xcor
            event.rotate_x = cls.rotate_x
            event.ycor = event.zcor = 0
            event.scale = 1
            cls.xcor += 1800
            cls.rotate_x += 90

    @classmethod
    def swoop_around(cls):
        cls.xcor = cls.ycor = cls.zor = cls.rotate_y = cls.rotate_x = 0

        for event in cls.events:
            event.xcor = cls.xcor
            event.rotate_y = cls.rotate_y
            event.rotate_x = cls.rotate_x
            event.ycor = event.zcor = 0
            event.scale = 1
            cls.xcor += 3000
            cls.rotate_y += 90
            cls.rotate_x += 90

    @classmethod
    def clusters(cls):
        cls.xcor = cls.ycor = cls.zcor = cls.rotate_y = cls.rotate_x = cls.rotate_z = 0
        cls.scale =1

        ranges = tuple(range(-6000, 6000, 1200))
        first = tuple(range(0, 500, 3))
        second = tuple(range(1, 500, 3))
        third = tuple(range(2, 500, 3))
        
        for index, event in enumerate(cls.events):
            event.scale = cls.scale
            cls.xcor = random.choice(ranges)
            cls.ycor = random.choice(ranges)
            cls.zcor = random.choice(ranges)


            if index in first:
                event.xcor = cls.xcor
                event.ycor = cls.ycor
                event.zcor = cls.zcor
                event.rotate_x = cls.rotate_x
                event.rotate_y = cls.rotate_y
                cls.rotate_x += 90
            elif index in second:
                event.rotate_x = cls.rotate_x
                cls.rotate_y += 90
            elif index in third:
                event.rotate_y = cls.rotate_y
                event.rotate_x = cls.rotate_x
                cls.rotate_y = 0
                cls.rotate_x = 0



    @classmethod
    def add_event(cls, event):
        cls.events.append(event)

    @classmethod
    def add_events(cls, events: list):
        for event in events:
            # print(event)
            an_event = Event(event)
            cls.add_event(an_event)
    
    @classmethod
    def list_events(cls):
        return cls.events

    @classmethod
    def length(cls):
        return len(cls.events)

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
