from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
}

REDIS_CONFIG = {
    "host": os.getenv("REDIS_HOST"),
    "port": int(os.getenv("REDIS_PORT"))
}