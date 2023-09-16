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
# import json
# import arrow

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MONTHS = ['Dec', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
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
all_events = kilton_events['events'] + leb_events['events']



branch = "KILTON"

k_events = []
xcor = 0
ycor = 0
rotate = 0

for event in all_events:
    # print(event)
    #xcor -= 1000 * random.randint(4,9) * len(kilton_events)
    # ycor += 1000 * random.randint(4,9) * len(kilton_events)
    ycor += 850
    scale = 1
    # rotate = random.randint(0,270)
    rotate += 45
    rotate *= -1
    # zcor = random.randint(-3000,3000)
    zcor = 0
    new_event = {}
    new_event['rotate'] = rotate
    new_event['scale'] = scale
    new_event['xcor'] = xcor
    new_event['ycor'] = ycor
    new_event['zcor'] = zcor
    new_event['title'] = event.get('title')
    date_obj = datetime.fromisoformat(event.get('start'))
    new_event['start_time'] = date_obj.time()
    new_event['weekday'] = WEEKDAYS[date_obj.weekday()]
    new_event['month'] = MONTHS[date_obj.month]
    new_event['day'] = date_obj.day
    # event_time = full_event_date.time()
    # new_event['time'] = event_time
    new_event['description'] = event.get('description')
    new_event['image'] = event.get('featured_image')
    new_event['campus'] = event.get('calendar').get('name')
    k_events.append(new_event)

# print(k_events)
# for event in k_events:
#     print(f"<div class=\"event\">")
#     print(f"<div class=\"title\">{event['title']}</div>")
#     print(f"<div class=\"time\">{event['time']}</div>")
#     # print(f"<div class=\"description\">{event['description']}</div>")
#     print(f"<div class=\"featured_image\"><img src=\"{event['image']}\">")
#     print("</div> <!-- end event --!>")
# print(k_events[0])
output = template.render({"branch": "Kilton", "events": k_events})
# print(output)

with open('test.html', 'w') as writer:
    writer.write(output)