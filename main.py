from dotenv import dotenv_values
import requests
import random
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Get env values
config = dotenv_values('.env')

# Setup Jinja2 Environment
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape()
)

template = env.get_template("impress.j2")

def sort_events_by_date(events):
    """Takes a list of event dicts and returns a sorted list of dict objects"""

    return sorted(unsorted_events, key=lambda x: x.get('start'))

def add_event_info(events):
    """Takes a list of event dicts and returns a new list of dicts with only the desired info"""

    events_info = []
    
    for event in events:
        event_info = {}
        event_info['title'] = event.get('title')
        start_time_obj = datetime.fromisoformat(event.get('start'))
        event_info['start_time'] = start_time_obj.strftime('%-I:%M %p')
        end_time_obj = datetime.fromisoformat(event.get('end'))
        event_info['end_time'] = end_time_obj.strftime('%-I:%M %p')
        event_info['weekday'] = start_time_obj.strftime('%A') 
        event_info['month'] = start_time_obj.strftime('%B')
        event_info['day'] = start_time_obj.day
        event_info['description'] = event.get('description')
        event_info['image'] = event.get('featured_image')
        event_info['campus'] = event.get('calendar').get('name').split(" ")[0]
        event_info['location'] = event.get('location').get('name')

        events_info.append(event_info)

    return events_info

def vertical_chain(events):
    """ Takes an unsorted list of event dicts and returns a list of dicts
    with info and positional data"""

    sorted_events = sort_events_by_date(events)
    computed_events = add_event_info(sorted_events)

    xcor, ycor, zcor, rotate = 0, 0, 0, 0
    
    for event in computed_events:
        ycor += 850
        scale = 1
        rotate += 45
        event['rotate'] = rotate
        event['scale'] = scale
        event['xcor'] = xcor
        event['ycor'] = ycor
        event['zcor'] = zcor
     
    return computed_events


r = requests.post('https://leblibrary.libcal.com/1.1/oauth/token',
                  json={"client_id": config['api-client-id'],
                        "client_secret": config['api-token'],
                        "grant_type": "client_credentials"})


access_token = r.json().get('access_token')

events_headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': f"Bearer {access_token}"}

kilton_events = requests.get('https://leblibrary.libcal.com/1.1/events?cal_id=15144', headers=events_headers).json()
leb_events = requests.get('https://leblibrary.libcal.com/1.1/events?cal_id=17790', headers=events_headers).json()


unsorted_events = kilton_events['events'] + leb_events['events']

new_events = vertical_chain(unsorted_events)


output = template.render({"events": new_events})

with open('output/test.html', 'w') as writer:
    writer.write(output)