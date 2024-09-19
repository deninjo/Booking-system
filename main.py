# Import the Customer class
from records import Customer  # Adjust the import based on your file structure

# Get customer details from user input
name = input("Enter name: ")
email = input("Enter email address: ")
phone_number = input("Enter phone number: ")
student = input("Is student? [0] No  [1] Yes : ")

# Create a Customer object
customer = Customer(name, email, phone_number, student)

# Save the customer details to the database
customer.save_to_db()
