import psycopg2

conn= psycopg2.connect(
    host = "localhost",
    user="mahlaka",
    password="",
    port = 5432,
    database="user_events_db"
    
)
cursor = conn.cursor()