import mysql.connector


def get_db_connection():
    try:
        # Establish a database connection
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='MySQLconnection99!',
            database='ticket_booking'
        )
        print("Connection successful.")
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
