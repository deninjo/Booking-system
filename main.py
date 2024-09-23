# Import the Customer class
from records import Customer, Movie, Theatre


# ------------------------------------------Customer-------------------------------------------------#
'''
'# Get customer details from user input
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
'''

'''
customer = Customer()
customer.input_details()
customer.save_to_db()
'''


# ---------------------------------MOVIE-------------------------------------------------#
'''
title = input("Enter movie title: ")
genre = input("Enter movie genre: ")
rating = input("Enter movie rating: ")
imdb = float(input("Enter imdb score: "))
duration = int(input("Enter duration in minutes: "))
year_of_release = int(input("Enter year of release: "))


# Create a Customer object
movie = Movie(title, genre, rating, imdb, duration, year_of_release)

# Save the customer details to the database
movie.save_to_db()
'''

'''movie = Movie()
movie.input_details()
movie.save_to_db()'''


# -------------------------------THEATRE-----------------------------------#
'''
# Example usage
layout = {
    'A': 10,
    'B': 10,
    'C': 12,
    'D': 14,
    'E': 14,
    'F': 14,
    'G': 16,
    'H': 16
}
{"A": 10, "B": 10, "C": 12, "D": 12, "E": 12, "F": 16, "G": 16}
theatre = Theatre()
theatre.input_details()
print("Theatre layout before saving to DB:", theatre.layout)  # Debug print
theatre.save_to_db()
theatre.get_seating_chart()
'''
theatre = Theatre()
theatre.input_details()
print("Theatre layout before saving to DB:", theatre.layout)  # Debug print
theatre.save_to_db()
theatre.get_seating_chart()
