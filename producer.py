from faker import Faker
import json
import random
import time
import random

fake = Faker()
event_types = ['click', 'view', 'purchase']

def generate_events():
    event = {
        "event_type": random.choice(event_types),
        "user_id":random.randint(1,1000),
        "timestamp":fake.iso8601(),
        "page" : fake.word()
    }
    return event
    
if __name__ == "main":
    while True:
        event = generate_events()
        json_event = json.dumps(event)
        print(json_event)
        time.sleep(1)
        
