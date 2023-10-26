from dotenv import dotenv_values
import requests
import random
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from events import Event

# Get env values
config = dotenv_values('.env')

# Setup Jinja2 Environment
env = Environment(
    loader=FileSystemLoader('templates'),
    trim_blocks=True,
    lstrip_blocks=True,
    autoescape=select_autoescape()
)

template = env.get_template("impress.j2")

r = requests.post('https://leblibrary.libcal.com/1.1/oauth/token',
                  json={"client_id": config['api-client-id'],
                        "client_secret": config['api-token'],
                        "grant_type": "client_credentials"})


access_token = r.json().get('access_token')

events_headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': f"Bearer {access_token}"}

kilton_events = requests.get('https://leblibrary.libcal.com/1.1/events?cal_id=15144', headers=events_headers).json()
leb_events = requests.get('https://leblibrary.libcal.com/1.1/events?cal_id=17790', headers=events_headers).json()


unsorted_events = kilton_events['events'] + leb_events['events']
print(unsorted_events[0]["start"])

Event.add_events(unsorted_events)
# for event in unsorted_events:
#     an_event = Event(event)
#     # print(an_event, len(an_event))
#     Event.add_event(an_event)
#     # print(Event.length())


# Event.vertical_chain()
# Event.horizontal_chain()
# Event.ring_twist()
# Event.ring_around()
# Event.clusters()
Event.arrange()

output = template.render({"events": Event.list_events()})

with open('output/index.html', 'w') as writer:
    writer.write(output)