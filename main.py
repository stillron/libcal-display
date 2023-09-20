from dotenv import dotenv_values
import requests
import random
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

config = dotenv_values('.env')

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape()
)

template = env.get_template("impress.j2")

r = requests.post('https://leblibrary.libcal.com/1.1/oauth/token',
                  json={"client_id": 1226,
                        "client_secret": config['api-token'],
                        "grant_type": "client_credentials"})


access_token = r.json().get('access_token')

events_headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': f"Bearer {access_token}"}

k_events_response = requests.get('https://leblibrary.libcal.com/1.1/events?cal_id=15144', headers=events_headers)

l_events_response = requests.get('https://leblibrary.libcal.com/1.1/events?cal_id=17790', headers=events_headers)
kilton_events = k_events_response.json()
leb_events = l_events_response.json()
unsorted_events = kilton_events['events'] + leb_events['events']
sorted_events = sorted(unsorted_events, key=lambda x: x.get('start'))


# print(sorted_events[0])

branch = "KILTON"

new_events = []
xcor = 0
ycor = 0
rotate = 0

for event in sorted_events:
    # if event.get('location').get('name') != "":
    #     print(event.get('location').get('name'))
    # else:
    #     print("Oops")
    #xcor -= 1000 * random.randint(4,9) * len(kilton_events)
    # ycor += 1000 * random.randint(4,9) * len(kilton_events)
    ycor += 850
    scale = 1
    # rotate = random.randint(0,270)
    rotate += 45
    # rotate *= -1
    # zcor = random.randint(-3000,3000)
    zcor = 0
    new_event = {}
    new_event['rotate'] = rotate
    new_event['scale'] = scale
    new_event['xcor'] = xcor
    new_event['ycor'] = ycor
    new_event['zcor'] = zcor
    new_event['title'] = event.get('title')
    start_time_obj = datetime.fromisoformat(event.get('start'))
    new_event['start_time'] = start_time_obj.strftime('%-I:%M %p')
    end_time_obj = datetime.fromisoformat(event.get('end'))
    new_event['end_time'] = end_time_obj.strftime('%-I:%M %p')
    new_event['weekday'] = start_time_obj.strftime('%A') 
    new_event['month'] = start_time_obj.strftime('%B')
    new_event['day'] = start_time_obj.day
    new_event['description'] = event.get('description')
    new_event['image'] = event.get('featured_image')
    new_event['campus'] = event.get('calendar').get('name').split(" ")[0]
    new_event['location'] = event.get('location').get('name')
    
    new_events.append(new_event)


output = template.render({"branch": "Kilton", "events": new_events})
# print(output)
print({"branch": "Kilton", "events": new_events})

with open('test.html', 'w') as writer:
    writer.write(output)