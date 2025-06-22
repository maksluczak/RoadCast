import mysql.connector
from mysql.connector import Error

def database_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="roadcast_db"
        )
        if conn.is_connected():
            print("Database connected successfully")
            return conn, conn.cursor()
    except Error as e:
        print("Error while connecting to database:", e)
        return None, None

def insert_data(weekday: int, hour: int, temperature: float, rain: float, traffic_volume: float, trip_duration_minutes:float, historical_travel_time:float):
    dbconn, dbcursor = database_connection()

    if not dbconn or not dbcursor:
        print("[ERROR] Failed to insert data: no database connection.")
        return
    
    try:
        sql = """
            INSERT INTO traffic_data (weekday, hour, temperature, rain, traffic_volume, trip_duration_minutes, historical_travel_time) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        val = (weekday, hour, temperature, rain, traffic_volume, trip_duration_minutes, historical_travel_time)
        dbcursor.execute(sql, val)
        dbconn.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"[ERROR] Failed to insert data: {e}")
    finally:
        dbcursor.close()
        dbconn.close()