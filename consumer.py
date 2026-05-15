import redis
import json
import time
import logging
from datetime import datetime
from db import conn, cursor
from config import REDIS_CONFIG

logging.basicConfig(level=logging.INFO)

redis_client = redis.Redis(**REDIS_CONFIG)

STREAM_NAME = "user_events"


def read():
    last_id = "0"

    while True:
        response = redis_client.xread(
            {STREAM_NAME: last_id},
            block=5000,
            count=1
        )

        if response:
            stream_name, events = response[0]

            for event_id, event_data in events:
                if "event" not in event_data:
                    logging.warning(f"Skipping unexpected Redis record: {event_data}")
                    last_id = event_id
                    continue

                json_event = event_data["event"]
                event = json.loads(json_event)

                logging.info(f"Received event: {event}")

                required_fields = ["user_id", "event_type", "page", "timestamp"]

                if any(field not in event or event[field] is None for field in required_fields):
                    logging.warning(f"Invalid event skipped: {event}")
                    continue

                event["event_type"] = event["event_type"].lower().strip()
                event["page"] = event["page"].lower().strip()
                processed_at = datetime.utcnow()

                cursor.execute(
                    """
                    INSERT INTO user_events
                    (user_id, event_type, page, timestamp, processed_at)
                    VALUES (%s, %s, %s, %s, %s)
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
                logging.info("Inserted into PostgreSQL")

                last_id = event_id

        else:
            logging.info("No new events...")
            time.sleep(1)


if __name__ == "__main__":
    read()