from db import conn, cursor

def run_daily_summary():
    cursor.execute("""
        INSERT INTO daily_event_summary
        (event_date, event_type, total_events, unique_users)
        SELECT
            DATE(timestamp) AS event_date,
            event_type,
            COUNT(*) AS total_events,
            COUNT(DISTINCT user_id) AS unique_users
        FROM user_events
        GROUP BY DATE(timestamp), event_type;
    """)

    conn.commit()
    print("Daily summary generated successfully")


if __name__ == "__main__":
    run_daily_summary()