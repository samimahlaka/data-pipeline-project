import redis
import json
import time

redis_client = redis.Redis(
    host = "localhost",
    port = 6379,
    decode_responses = True
)

STREAM_NAME = "user_events"

def read():
    last_id = "0"
    
    while True:
        response = redis_client.xread(
            {STREAM_NAME : last_id},
            block  =5000,
            count= 1
        )
        
        if response:
            for stream,events in response:
                stream_name, event = response[0]
                
                for event_id, event_data in event:
                    json_event = event_data["event"]
                    event= json.loads(json_event)
                    print("Received event:", event)
                    last_id = event_id
                    
        
if __name__ == "__main__":
    read()