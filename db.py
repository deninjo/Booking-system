import os
import mysql.connector

# Retrieve the password from the environment variable
mysql_password = os.getenv("MYSQL_PASSWORD")

def get_db_connection():
    global mysql_password
    try:
        # Establish a database connection
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password=mysql_password,
            database='ticket_booking',

        )
        print(".")
        return mydb

    # Error message if the connection fails
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def show_tables():
    mydb = get_db_connection()
    if mydb is None:
        print("Failed to connect to the database")
        return

    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        print(x)

    mycursor.close()
    mydb.close()



get_db_connection()