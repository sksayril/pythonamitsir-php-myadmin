import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="phython"  # Connect directly to this database
    )

    if connection.is_connected():
        print("Connected to MySQL server and database 'phython'")
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        
        print("Tables in 'phython' database:")
        for table in cursor:
            print(table[0])
        
        cursor.close()
        connection.close()
    else:
        print("Connection failed.")

except Error as e:
    print(f"Error: {e}")
