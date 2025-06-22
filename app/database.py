import mysql.connector
from mysql.connector import Error
import csv
import os

os.makedirs('./exports', exist_ok=True)

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

def insert_data(weekday: int, hour: int, temperature: float, rain: float, traffic_volume: float, route_length:float, trip_duration_minutes:float):
    dbconn, dbcursor = database_connection()

    if not dbconn or not dbcursor:
        print("[ERROR] Failed to insert data: no database connection.")
        return
    
    sql = """
            INSERT INTO traffic_data (weekday, hour, temperature, rain, traffic_volume, route_length, trip_duration_minutes) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
    val = (weekday, hour, temperature, rain, traffic_volume, route_length, trip_duration_minutes)

    try:
        dbcursor.execute(sql, val)
        dbconn.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"[ERROR] Failed to insert data: {e}")
    finally:
        dbcursor.close()
        dbconn.close()

def database_to_csv():
    dbconn, dbcursor = database_connection()

    if not dbconn or not dbcursor:
        print("[ERROR] Failed to connect to database.")
        return
    
    sql = "SELECT * FROM traffic_data"
    csv_file_path = './exports/traffic_data.csv'

    try:
        dbcursor.execute(sql)
        rows = dbcursor.fetchall()
        column_names = [i[0] for i in dbcursor.description]
    except Error as e:
        print(f"[ERROR] Failed to retrieve data: {e}")
        return
    finally:
        dbcursor.close()
        dbconn.close()

    if rows:
        with open(csv_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(column_names)
            csvwriter.writerows(rows)
        print("Data exported to CSV successfully.")
    else:
        print("[INFO] No rows found to export.")