import json
import requests
import random
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from events import Event
import os
import boto3

API_CLIENT_ID = os.environ['api_client_id']
API_TOKEN = os.environ['api_token']
s3 = boto3.client('s3')


def lambda_handler(event, context):
    response = main_func()
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def main_func():
    bucket = 'events-display'
    file_name = 'index.html'


    
    # Setup Jinja2 Environment
    env = Environment(
        loader=FileSystemLoader('templates'),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=select_autoescape()
    )
        
    template = env.get_template("impress.j2")
    
    r = requests.post('https://leblibrary.libcal.com/1.1/oauth/token',
                      json={"client_id": API_CLIENT_ID,
                            "client_secret": API_TOKEN,
                            "grant_type": "client_credentials"})
    
    
    access_token = r.json().get('access_token')
    
    events_headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': f"Bearer {access_token}"}
    
    response = requests.get('https://leblibrary.libcal.com/1.1/events?cal_id=15144', headers=events_headers)
    kilton_reponse_code = response.status_code
    kilton_events = response.json()
    
    response = requests.get('https://leblibrary.libcal.com/1.1/events?cal_id=17790', headers=events_headers)
    lebanon_response_code = response.status_code
    leb_events = response.json()


    unsorted_events = kilton_events['events'] + leb_events['events']
    
    
    Event.add_events(unsorted_events)
    number_of_events = len(Event.events)

    Event.arrange()
    
    output = template.render({"events": Event.list_events()})

    with open('/tmp/index.html', 'w') as writer:
        writer.write(output)
    
    s3.upload_file('/tmp/index.html', bucket, file_name,
        ExtraArgs={'ContentType': 'text/html'})
        
    # Reinitialize class variables to account for lambda caching
    Event.events = []
    Event.rotate_x = Event.rotate_y = Event.rotate_z = Event.scale = None
    Event.xcor = Event.ycor = Event.zcor = None
        
    
    status = {
        "kilton_response": kilton_reponse_code,
        "lebanon_response": lebanon_response_code,
        "num_events": number_of_events,
    }
    return status
    