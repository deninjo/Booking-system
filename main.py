# Import the Customer class
from records import Customer, Movie, Theatre, Showtime, Seat, Price, Booking
'''

customer = Customer()
customer.input_details()
customer.save_to_db()
'''

movie = Movie()
movie.display_available_movies_with_showtimes()

booking = Booking()
booking.create_booking()


