# Import the Customer class
from records import Customer  # Adjust the import based on your file structure

# Get customer details from user input
name = input("Enter name: ")
email = input("Enter email address: ")
while True:
    phone_number = input("Enter phone number: ")
    if len(phone_number) == 10 and phone_number.isdigit():
        break
    else:
        print("Phone number should contain exactly 10 digits and be numeric.")

while True:
    student = input("Is student? [0] No  [1] Yes : ")
    if student in ['0', '1']:
        break
    else:
        print("Invalid input! Please enter '0' for No or '1' for Yes.")

# Create a Customer object
customer = Customer(name, email, phone_number, student)

# Save the customer details to the database
customer.save_to_db()
