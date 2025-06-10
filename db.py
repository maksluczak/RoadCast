import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='roadcast_db'
)

cursor = mydb.cursor()
print("Database connected successfully")

mycursor = mydb.cursor()