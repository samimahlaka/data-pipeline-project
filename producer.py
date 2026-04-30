from faker import Faker
import json
import random
import time
import redis
import random

fake = Faker()
event_types = ['click', 'view', 'purchase']

redis_client = redis.Redis(
    host = "localhost",
    port = 6379,
    decode_responses = True
)

STREAM_NAME = "user_events"
def generate_events():
    event = {
        "event_type": random.choice(event_types),
        "user_id":random.randint(1,1000),
        "timestamp":fake.iso8601(),
        "page" : fake.word()
    }
    return event
    
if __name__ == "__main__":
    while True:
        event = generate_events()
        
        redis_client.xadd(
            STREAM_NAME,
            {"event" : json.dumps(event)}
        )
        print("Sent event:", event)
        time.sleep(1)
        
