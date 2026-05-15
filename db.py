import psycopg2
from config import POSTGRES_CONFIG

conn= psycopg2.connect(
    **POSTGRES_CONFIG
    
)
cursor = conn.cursor()