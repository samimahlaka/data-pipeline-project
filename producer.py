from faker import Faker
import json
import random
import time
import redis
import logging
from config import REDIS_CONFIG

logging.basicConfig(level=logging.INFO)

fake = Faker()
event_types = ["click", "view", "purchase"]

redis_client = redis.Redis(**REDIS_CONFIG)

STREAM_NAME = "user_events"


def generate_events():
    event = {
        "event_type": random.choice(event_types),
        "user_id": random.randint(1, 1000),
        "timestamp": fake.iso8601(),
        "page": fake.word()
    }
    return event


if __name__ == "__main__":
    while True:
        event = generate_events()

        redis_client.xadd(
            STREAM_NAME,
            {"event": json.dumps(event)}
        )

        logging.info(f"Sent event: {event}")
        time.sleep(1)