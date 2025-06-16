import mysql.connector
from mysql.connector import Error

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database='roadcast_db'
    )
    if mydb.is_connected():
        cursor = mydb.cursor()
        print("Database connected successfully")
    
except Error as e:
    print("Error while connecting to database: " + e)