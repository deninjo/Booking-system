# Import the Customer class
from records import Customer, Movie, Theatre, Showtime, Seat, Price, Booking


from records import Customer, Movie, Theatre, Seat, Booking

def main():
    # Step 1: Create a Customer object and input detaills

    '''
    customer = Customer()
    customer.input_details()
    customer.save_to_db()
    '''



    # Step 2: Create a Movie object and display available movies with showtimes


    # Step 3: Select a movie and showtime for booking
    booking = Booking()
    booking.create_booking()
    '''
    # Step 4: Lookup the booking table to get theatre ID and booked seats
    theatre = Theatre()
    booked_seats = theatre.fetch_booked_seats()

    # Step 5: Display the selected theatre's seat chart with booked seats marked
    theatre.get_seating_chart(booked_seats)

    # Step 6: Allow user to select a seat
    selected_seat = input("Enter the Seat ID to book: ")

    # Step 7: Check if the selected seat exists in the seat table
    if not theatre.check_seat_exists(selected_seat):
        theatre.save_new_seat(selected_seat)  # Create a new seat instance

    # Step 8: Save the booking with status 'Confirmed'
    booking = Booking(customer.customer_id, showtime_id, movie_id, theatre.theatre_id, selected_seat)
    booking.save_to_db(status='Confirmed')

    # Step 9: Allow user to remove a selected seat
    remove_seat = input("Do you want to remove a selected seat? (yes/no): ")
    if remove_seat.lower() == 'yes':
        booking.update_status(selected_seat, 'Cancelled')  # Update the booking status to 'Cancelled'

'''


if __name__ == "__main__":
    main()




