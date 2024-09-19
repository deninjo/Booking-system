from db import get_db_connection


class Customer:
    def __init__(self, name, email, phone_number, student):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.student = student

    def save_to_db(self):
        # Use centralized db connection from get_db_connection()
        mydb = get_db_connection()
        if mydb is None:
            print("Failed to connect to the database.")
            return

        mycursor = mydb.cursor()

        # SQL query to insert customer details
        insert = ("INSERT INTO customer (name, email, phone_number, student) "
                  "VALUES (%s, %s, %s, %s)")
        values = (self.name, self.email, self.phone_number, self.student)

        try:
            # Execute and commit
            mycursor.execute(insert, values)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Close cursor and connection
            mycursor.close()
            mydb.close()


# Get customer details from user input
name = input("Enter name: ")
email = input("Enter email address: ")
phone_number = input("Enter phone number: ")
student = input("Is student? [0] No  [1] Yes : ")

# Create a Customer object
customer = Customer(name, email, phone_number, student)

# Save the customer details to the database
customer.save_to_db()
