from records import Customer, Movie, Showtime, Price, Booking


def login():
    """
    Handles user login and determines access panel.
    Returns: role (str) - 'manager' or 'cashier'
    """
    print("\n======= Main Menu ========")
    print("1. Manager")
    print("2. Cashier")
    role = input("Select your role : ").strip()

    if role == "1":
        print("Accessing Manager's Panel...")
        return "manager"
    elif role == "2":
        print("Accessing Cashier's Panel...")
        return "cashier"
    else:
        print("Invalid selection. Please try again.")
        return login()


def manager_panel():
    """
    Manager-specific functionalities: Add movies, showtimes, and alter prices.
    """
    print("\n======= Manager's Panel =======")
    while True:
        print("\n1. Add a Movie")
        print("2. Add a Showtime")
        print("3. Alter Ticket Price")
        print("4. Exit Manager Panel")
        choice = input("Select an option: ").strip()

        if choice == "1":
            try:
                print("")
                movie = Movie()
                movie.input_details()
                movie.save_to_db()
                print("Movie added successfully!")
            except Exception as e:
                print(f"An error occurred while adding the movie: {e}")

        elif choice == "2":
            try:
                print("")
                showtime = Showtime()
                showtime.input_details()
                showtime.save_to_db()
                print("Showtime added successfully!")
            except Exception as e:
                print(f"An error occurred while adding the showtime: {e}")

        elif choice == "3":
            try:
                print("")
                price = Price()
                print("Feature under construction. Implement alter_price logic here.")
                # Placeholder for the alter_price functionality
                # price.alter_price()
            except Exception as e:
                print(f"An error occurred while altering the ticket price: {e}")

        elif choice == "4":
            print("Exiting Manager Panel.")
            break

        else:
            print("Invalid choice. Please try again.")


def cashier_panel():
    """
    Cashier-specific functionalities: Handle customer and booking creation.
    """
    print("\n======= Cashier's Panel =======")
    while True:
        print("\n1. Handle a Booking")
        print("2. Exit Cashier Panel")
        choice = input("Select an option: ").strip()

        if choice == "1":
            try:
                # Create a Customer and Booking object
                print("")

                # Step 1: Enquire if the customer is new or registered
                customer_type = input("Is the customer registered? [y/n]: ").strip().lower()

                if customer_type == 'y':  # Existing customer
                    phone_number = input("Enter the customer's phone number: ").strip()

                    # Check if the customer exists in the database
                    customer = Customer()
                    customer_id, name = customer.get_customer_details_by_phone(phone_number)

                    if customer_id:
                        print(f"Customer found! Name: {name}, Customer ID: {customer_id}")

                        booking = Booking()
                        booking.create_booking(customer_id)
                        print("Booking completed successfully!")

                    else:
                        print("No customer found with the provided phone number.")
                        return  # Exit if no customer is found




                else:  # New customer
                    customer = Customer()
                    customer.input_details()
                    customer.save_to_db()
                    print("Customer details saved successfully!")

                    booking = Booking()
                    booking.create_booking()
                    print("Booking completed successfully!")




            except Exception as e:
                print(f"An error occurred during booking: {e}")

        elif choice == "2":
            print("Exiting Cashier Panel.")
            break

        else:
            print("Invalid choice. Please try again.")


def main():
    """
    Main entry point for the application.
    """
    print("\n\t\t\t\t\t\t\t\t\t\t ~ WELCOME TO BROADWAY CLASSICAL THEATRE ~ ")
    role = login()

    if role == "manager":
        manager_panel()
    elif role == "cashier":
        cashier_panel()
    else:
        print("Invalid role. Exiting the system.")


if __name__ == "__main__":
    main()
