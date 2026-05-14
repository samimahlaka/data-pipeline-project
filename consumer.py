import redis
import json
import time
from db import conn,cursor
import datetime

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
                    required_fields = ["user_id", "event_type", "page", "timestamp"]

                    for field in required_fields:
                        if field not in event or event[field] is None:
                            print("Invalid event skipped:", event)
                            continue

                    # Transform event
                    event["event_type"] = event["event_type"].lower().strip()
                    event["page"] = event["page"].lower().strip()
                    processed_at = datetime.utcnow()
                    cursor.execute(
                    """
                    INSERT INTO user_events (user_id, event_type, page, timestamp)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        event["user_id"],
                        event["event_type"],
                        event["page"],
                        event["timestamp"],
                        processed_at
                    )
                )

                conn.commit()
                print("Inserted into PostgreSQL")
            last_id = event_id
                    
        
if __name__ == "__main__":
    read()