# import seats
import mysql.connector
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password="MySQLconnection99!",
    database='ticket_booking'
)

# showing database tables
mycursor = mydb.cursor()
mycursor.execute("SHOW TABLES")
for x in mycursor:
    print(x)

mydb.commit()


# Entering customer details
name = input("Enter name: ")
email = input("Enter email address: ")
phone_number = input("Enter phone number: ")
student = input("Is student? [0]No  [1]Yes : ")

insert = ("INSERT INTO customer_details(name, email, phone_number, student)"
          "VALUES"
          "(%s, %s, %s, %s) ")
values = (name, email, phone_number, student)
mycursor.execute(insert, values)

mydb.commit()
print()

print(mycursor.rowcount, "record inserted.")