import re
import json
import string
from datetime import datetime
from db import get_db_connection


class Customer:
    def __init__(self, name="", email="", phone_number="", student=0):
        # Initializes the customer object with default values for customer details
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.student = student

    def input_details(self):
        # Prompts the user to enter their customer details
        self.name = input("Enter name: ")

        # Email validation
        self.email = input("Enter email address: ")
        while not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            print("Invalid email format. Please try again.")
            self.email = input("Enter email address: ")

        self.phone_number = input("Enter phone number (10 digits): ")

        # Ensure phone number is 10 digits
        while len(self.phone_number) != 10 or not self.phone_number.isdigit():
            print("Phone number should contain exactly 10 digits.")
            self.phone_number = input("Enter phone number (10 digits): ")

        self.student = input("Is student? [0] No  [1] Yes: ")

        # Validate student status
        while self.student not in ['0', '1']:
            print("Invalid input. Please enter 0 for No or 1 for Yes.")
            self.student = input("Is student? [0] No  [1] Yes: ")

    def save_to_db(self):
        # Saves the customer details to the database using a predefined SQL insert query
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


    def get_customer_details_by_phone(self, phone_number):
        """Retrieve customer details (ID and name) based on phone number."""
        mydb = get_db_connection()
        if not mydb:
            print("Database connection failed.")
            return None, None  # Return None for both ID and name

        try:
            cursor = mydb.cursor()
            query = "SELECT customer_id, name FROM customer WHERE phone_number = %s"
            cursor.execute(query, (phone_number,))
            result = cursor.fetchone()
            if result:
                return result[0], result[1]  # Return customer_id and name
            else:
                return None, None  # No customer found
        except Exception as e:
            print(f"Error retrieving customer details: {e}")
            return None, None
        finally:
            cursor.close()
            mydb.close()


class Movie:
    def __init__(self, title="", genre="", rating="", imdb="", duration="", year_of_release=""):
        # Initializes the movie object with default values for movie details
        self.title = title
        self.genre = genre
        self.rating = rating
        self.imdb = imdb
        self.duration = duration
        self.year_of_release = year_of_release

    def input_details(self):
        # Prompts the user to enter movie details
        self.title = input("Enter movie title: ")
        self.genre = input("Enter movie genre: ")
        self.rating = input("Enter movie rating: ")
        self.imdb = float(input("Enter imdb score: "))
        self.duration = (input("Enter duration in minutes: "))

        # Ensuring duration is a positive integer
        while not self.duration.isdigit():
            print("Duration should be a positive integer")
            self.duration = input("Enter duration in minutes: ")

        self.duration = int(self.duration) # <--- Move outside the loop
        self.year_of_release = int(input("Enter year of release: "))

    def save_to_db(self):
        # Saves the movie details to the database using a predefined SQL insert query

        # Use centralized db connection from get_db_connection()
        mydb = get_db_connection()
        if mydb is None:
            print("Failed to connect to the database.")
            return

        mycursor = mydb.cursor()

        # SQL query to insert movie details
        insert = ("INSERT INTO movie (title, genre, rating, imdb, duration, year_of_release) "
                  "VALUES (%s, %s, %s, %s, %s, %s)")
        values = (self.title, self.genre, self.rating, self.imdb, self.duration, self.year_of_release)

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

    def get_showtimes(self):
        # Retrieves showtimes for the current movie from the database

        # Use centralized db connection from get_db_connection()
        mydb = get_db_connection()
        if mydb is None:
            print("Failed to connect to the database.")
            return False

        try:
            mycursor = mydb.cursor(dictionary=True)

            # SQL query to retrieve showtimes for movies
            select = """
            SELECT show_time.showtime_id, movie.movie_id, movie.title, movie.genre, movie.IMDB, 
                   theatre.theatre_id, theatre.screen, show_time.start_time, 
                   show_time.show_date
            FROM show_time
            JOIN movie ON show_time.movie_id = movie.movie_id
            JOIN theatre ON show_time.theatre_id = theatre.theatre_id;
            """
            mycursor.execute(select)
            results = mycursor.fetchall()  # Fetch all matching records

            # If valid records are found, process and display them
            if results:
                showtimes = []
                for result in results:
                    # a dictionary is created for each row.
                    showtime_record = {
                        "showtime_id": result["showtime_id"],
                        "movie_id": result["movie_id"],
                        "title": result["title"],
                        "genre": result["genre"],
                        "IMDB": result["IMDB"],
                        "theatre_id": result["theatre_id"],
                        "screen": result["screen"],
                        "start_time": result["start_time"],
                        "show_date": result["show_date"]
                    }
                    showtimes.append(showtime_record)

                return showtimes  # Return the list of showtime records
            else:
                print("No showtimes found.")
                return []

        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            # Close cursor and connection
            mycursor.close()
            mydb.close()

    def display_available_movies_with_showtimes(self):
        # Displays the available movies with their corresponding showtimes

        showtimes = self.get_showtimes()  # Get showtimes for the movie

        if not showtimes:
            print("No showtimes available.")
            return

        # Grouping by movie title for better display
        movies = {}
        for showtime in showtimes:
            title = showtime["title"]
            movie_id = showtime["movie_id"]
            genre = showtime["genre"]
            imdb = showtime["IMDB"]
            if title not in movies:
                movies[title] = {
                    "movie_id": movie_id,
                    "genre": genre,
                    "IMDB": imdb,
                    "showtimes": []
                }
            movies[title]["showtimes"].append(showtime)

        # Displaying the movies with their showtimes
        print("\t\t\t\t\t~Available Movies with their Showtimes:")
        for title, data in movies.items():
            movie_id = data["movie_id"]
            genre = data["genre"]
            imdb = data["IMDB"]
            print(f"\nMovie: {title}   ID: {movie_id}   Genre: {genre}   IMDB: {imdb}")
            for showtime in data["showtimes"]:
                print(f"    Showtime ID: {showtime['showtime_id']}, "
                      f"Theatre: {showtime['theatre_id']}, "
                      f"Screen: {showtime['screen']}, "
                      f"Date: {showtime['show_date']}, "
                      f"Start Time: {showtime['start_time']}")


class Theatre:
    def __init__(self, theatre_id="", screen="", layout=None):
        # Initializes the theatre object with default values for theatre details
        self.theatre_id = theatre_id
        self.screen = screen
        self.layout = layout if layout else {}  # Ensures that self.layout always holds a valid dictionary

    def load_from_db(self, theatre_id):
        # Loads the theatre details from the database using the provided theatre_id.
        # Sets the theatre_id, screen, and layout for the object.
        # Returns True if the theatre details are successfully loaded; False otherwise.

        mydb = get_db_connection()
        if mydb is None:
            print("Failed to connect to the database.")
            return False

        try:
            mycursor = mydb.cursor(dictionary=True)
            select = "SELECT * FROM theatre WHERE theatre_id = %s"
            mycursor.execute(select, (theatre_id,))
            result = mycursor.fetchone()

            if result:
                self.theatre_id = result["theatre_id"]
                self.screen = result["screen"]
                layout_str = result["layout"]

                if layout_str:
                    try:
                        self.layout = json.loads(layout_str)
                    except json.JSONDecodeError:
                        print(f"Invalid JSON format in layout: {layout_str}")
                        return False
                else:
                    print("Layout is empty. Please provide a valid layout.")
                    return False

                return True
            else:
                print("Theatre not found.")
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        finally:
            mycursor.close()
            mydb.close()

    def get_seating_chart(self, selected_seats, showtime_id):
        # Displays the seating chart for the theatre, with booked seats marked as '**'.
        # The selected seats are passed in and displayed alongside the booked seats.

        # Get booked seats from the database
        booked_seats = set(self.fetch_booked_seats(showtime_id))

        # Add newly selected seats to the booked seats for this display
        booked_seats.update(selected_seats)  # Using a set for efficient lookups

        print(f"\n{' ' * 35}THEATRE {self.theatre_id}")
        print("             ====================================================")
        print("                                   SCREEN")
        print("             ====================================================")

        if not self.layout:
            print("Layout is empty. Please provide a valid layout.")
            return

        max_range = max(self.layout.values())
        rows = len(self.layout)

        seat = string.ascii_uppercase

        for i in range(rows):
            row_letter = seat[i]
            num_seats = self.layout.get(row_letter, 0)
            seats = [f"{row_letter}{j}" for j in range(1, num_seats + 1)]

            # Mark the booked seats with **
            for booked_seat in booked_seats:
                if booked_seat in seats:
                    seats[seats.index(booked_seat)] = "**"

            # Create the row display
            seat_row = '  '.join(seats)
            seat_row_width = len(seat_row)
            padding = (max_range * 5 - seat_row_width) // 2

            print((' ' * padding) + seat_row)

    def fetch_booked_seats(self, showtime_id):
        """Fetch booked seats for a specific showtime.
        Returns:
            set: A set of booked seat IDs.
        """
        booked_seats = list(set())  # Initialize an empty set to hold booked seats
        mydb = get_db_connection()
        if mydb is None:
            print("Failed to connect to the database.")
            return booked_seats
        try:
            mycursor = mydb.cursor()
            query = """
            SELECT booked_seat FROM booking 
            WHERE showtime_id = %s AND theatre_id = %s AND status = 'Confirmed'
            """
            mycursor.execute(query, (showtime_id, self.theatre_id))

            # Fetch all booked seats and add them to the set
            results = mycursor.fetchall()
            for result in results:
                booked_seats.extend(result[0].split(', '))  # Assuming booked_seat is a comma-separated string

        except Exception as e:
            print(f"An error occurred while retrieving booked seats: {e}")

        finally:
            mycursor.close()
            mydb.close()

        return booked_seats


class Showtime:
    def __init__(self, showtime_id="", movie_id="", theatre_id="", show_date="", start_time=""):
        # Initializes the showtime object with default values for showtime details
        self.showtime_id = showtime_id
        self.movie_id = movie_id
        self.theatre_id = theatre_id
        self.show_date = show_date
        self.start_time = start_time

    def input_details(self):
        # Prompts the user to enter showtime details
        self.showtime_id = input("Enter Show Time ID (e.g WE-N): ").strip().upper()
        self.movie_id = input("Enter movie id (e.g 701): ")
        self.theatre_id = input("Enter theatre id (e.g IIB): ").strip().upper()
        self.show_date = input("Enter date (dd/mm/yyyy): ")
        self.show_date = datetime.strptime(self.show_date, "%d/%m/%Y").date()
        self.start_time = input("Enter time (hh:mm): ")
        self.start_time = datetime.strptime(self.start_time, "%H:%M").time()

    def save_to_db(self):
        # Saves the showtime details to the database using a predefined SQL insert query

        # Use centralized db connection from get_db_connection()
        mydb = get_db_connection()
        if mydb is None:
            print("Failed to connect to the database.")
            return

        mycursor = mydb.cursor()

        # SQL query to insert movie details
        insert = ("INSERT INTO show_time (showtime_id, movie_id, theatre_id, show_date, start_time) "
                  "VALUES (%s, %s, %s, %s, %s)")
        values = (self.showtime_id, self.movie_id, self.theatre_id, self.show_date, self.start_time)

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


class Seat:
    def __init__(self, theatre_instance):
        # Initializes the Seat object, holding a reference to the Theatre instance.
        # The selected_seats list will keep track of the seats the user selects.

        self.theatre = theatre_instance # Reference to the Theatre instance
        self.selected_seats = []

    def select_seat(self, showtime_id):
        # Allows the user to select seats for a specific showtime.
        # Displays the seating chart and prompts for seat selection, checking for valid inputs and booked seats.

        booked_seats = self.theatre.fetch_booked_seats(showtime_id)
        self.theatre.get_seating_chart(booked_seats, showtime_id)

        self.selected_seats = []
        while True:

            # Prompt the user to select a seat
            selected_seat = input("\nSelect a seat (e.g., A1) or type 'q' to quit: ").strip().upper()

            if selected_seat.lower() == 'q':
                break

            # Extract row letter and seat number
            if len(selected_seat) > 1:
                row = selected_seat[0]
                number = selected_seat[1:]

                # Validate the seat selection
                if row in self.theatre.layout and number.isdigit() and 1 <= int(number) <= self.theatre.layout[row]:
                    if selected_seat not in self.selected_seats:
                        # Check if the seat is already booked in the database
                        if not self.is_seat_booked(selected_seat, showtime_id):
                            # Add the seat to the list of selected seats
                            self.selected_seats.append(selected_seat)
                            print(f"Seat {selected_seat} selected.")

                            # Display the seating chart with the newly selected seat marked
                            self.theatre.get_seating_chart(booked_seats + self.selected_seats, showtime_id)  # Update with booked + selected
                        else:
                            print("Seat is already booked. Choose a different seat.")
                    else:
                        print("Seat already selected. Choose a different seat.")
                else:
                    print("Invalid seat number. Please try again.")
            else:
                print("Invalid seat format. Please try again.")

        if self.selected_seats:
            print(f"Your selected seats are: {self.selected_seats}")
        else:
            print("No selected seats.")

    def is_seat_booked(self, seat_id, showtime_id):
        """
        Checks if the given seat is already booked for the specific showtime and theatre.
        Returns True if booked, otherwise False.
        """
        mydb = get_db_connection()
        if mydb is None:
            print("Failed to connect to the database.")
            return False

        try:
            mycursor = mydb.cursor()
            query = """
                SELECT COUNT(*) FROM booking 
                WHERE booked_seat LIKE %s AND status = 'Confirmed' 
                  AND showtime_id = %s AND theatre_id = %s
            """
            mycursor.execute(query, (seat_id, showtime_id, self.theatre.theatre_id))
            return mycursor.fetchone()[0] > 0
        except Exception as e:
            print(f"An error occurred while checking seat availability: {e}")
            return False
        finally:
            mycursor.close()
            mydb.close()


class Price:
    def __init__(self, price_id="", showtime_id="", seat_category="", price=0):
        # Initializes the price object with default values for price details
        self.price_id = price_id
        self.showtime_id = showtime_id
        self.seat_category = seat_category
        self.price = price

    def load_from_db(self, showtime_id):
        # Loads the price details from the database based on the provided showtime_id

        # Use centralized db connection from get_db_connection()
        mydb = get_db_connection()
        if mydb is None:
            print("Failed to connect to the database.")
            return False

        try:
            mycursor = mydb.cursor(dictionary=True)

            # SQL query to retrieve price details for a specific showtime
            select = "SELECT * FROM price WHERE showtime_id = %s"
            mycursor.execute(select, (showtime_id,))
            results = mycursor.fetchall()  # Fetch all matching records

            # If valid records are found, load them into the object
            if results:
                for result in results:
                    price_record = Price()  # Create a new Price object for each record
                    price_record.price_id = result["price_id"]
                    price_record.showtime_id = result["showtime_id"]
                    price_record.seat_category = result["seat_category"]
                    price_record.price = result["price"]

                    # You might want to store these records in a list or do something with them
                    print(f"Loaded Price Record: ID={price_record.price_id}, Showtime={price_record.showtime_id}, "
                          f"Category={price_record.seat_category}, Price={price_record.price}")

                return True
            else:
                print(f"No prices found for Showtime ID: {showtime_id}")
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        finally:
            # Close cursor and connection
            mycursor.close()
            mydb.close()

    def alter_price(self):
        mydb = get_db_connection()
        if mydb is None:
            print("Failed to connect to the database.")
            return

        try:
            mycursor = mydb.cursor(dictionary=True)

            # Step 1: List distinct showtimes with their seat categories
            mycursor.execute("SELECT DISTINCT showtime_id FROM price")
            showtimes = mycursor.fetchall()

            if not showtimes:
                print("No price records available.")
                return

            print("\nAvailable Showtimes:")
            for idx, showtime in enumerate(showtimes, start=1):
                print(f"{idx}. {showtime['showtime_id']}")

            choice = input("Select a showtime by ID: ").strip().upper()

            # Step 2: Show current prices for that showtime
            query = "SELECT * FROM price WHERE showtime_id = %s"
            mycursor.execute(query, (choice,))
            prices = mycursor.fetchall()

            if not prices:
                print(f"No prices found for showtime {choice}")
                return

            print("\nCurrent Prices:")
            for idx, p in enumerate(prices, start=1):
                print(f"{idx}. ID: {p['price_id']} | Seat Category: {p['seat_category']} | Price: {p['price']}")

            price_id = input("\nEnter Price ID to update: ").strip().upper()

            # Step 3: Check if price_id exists
            mycursor.execute("SELECT * FROM price WHERE price_id = %s", (price_id,))
            existing = mycursor.fetchone()
            if not existing:
                print(f"No price record found with ID: {price_id}")
                return

            # Step 4: Get and validate new price
            new_price_input = input("Enter new price: ").strip()
            try:
                new_price = float(new_price_input)
                if not (100 <= new_price <= 5000):  # Set an appropriate range
                    print("Price should be between 100 and 5000.")
                    return
            except ValueError:
                print("Invalid price value.")
                return

            # Step 5: Update price
            update_query = "UPDATE price SET price = %s WHERE price_id = %s"
            mycursor.execute(update_query, (new_price, price_id))
            mydb.commit()

            print("Price updated successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            mydb.rollback()
        finally:
            mycursor.close()
            mydb.close()


class Booking:
    def __init__(self, booking_id="", customer_id="", showtime_id="", movie_id="", theatre_id="", booked_seat="", status=""):
        # Initializes the booking object with default values for booking details
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.showtime_id = showtime_id
        self.movie_id = movie_id
        self.theatre_id = theatre_id
        self.booked_seat = booked_seat
        self.status = status
        self.theatre = Theatre()

    def increment_string(self, s):
        # Increments the booking ID by 1 and formats it as a three-digit string with leading zeros.

        prefix = s[:-3]  # Extract the prefix ('B')
        number = int(s[-3:])  # Extract the number ('001') and convert to int
        incremented_number = number + 1
        return f"{prefix}{incremented_number:03d}"  # Returns three-digit string with leading zeros

    def get_last_customer_id(self):
        # Retrieves the last customer ID from the database.
        mydb = get_db_connection()
        if mydb is None:
            print("Failed to connect to the database.")
            return None

        try:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT customer_id FROM customer ORDER BY customer_id DESC LIMIT 1")
            result = mycursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            mycursor.close()
            mydb.close()

    def get_last_booking_id(self):
        # Retrieves the last booking ID from the database and returns a default "B000" if none is found.
        mydb = get_db_connection()
        if mydb is None:
            print("Failed to connect to the database.")
            return None

        try:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT booking_id FROM booking ORDER BY booking_id DESC LIMIT 1")
            result = mycursor.fetchone()
            return result[0] if result else "B000"
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            mycursor.close()
            mydb.close()

    def seat_exists(self, seat_id):
        """Check if the seat exists in the seat table."""
        mydb = get_db_connection()
        if mydb is None:
            print("Failed to connect to the database.")
            return None

        try:
            mycursor =mydb.cursor()
            query = "SELECT COUNT(*) FROM seat WHERE seat_id = %s"
            mycursor.execute(query, (seat_id,))
            exists = mycursor.fetchone()[0] > 0
        except Exception as e:
            print(f"An error occurred while checking for seat existence: {e}")
            exists = False
        finally:
            mycursor.close()
        return exists

    def insert_seat(self, seat_id, theatre_id):
        """Insert a new seat into the seat table."""
        row_letter = seat_id[0]  # Assuming seat_id is formatted as 'F2', extract 'F'
        number = int(seat_id[1:])

        mydb = get_db_connection()
        if mydb is None:
            print("Failed to connect to the database.")
            return None

        try:
            mycursor = mydb.cursor()
            query = "INSERT INTO seat (seat_id, theatre_id, row_letter, number) VALUES (%s, %s, %s, %s)"
            mycursor.execute(query, (seat_id, theatre_id, row_letter, number))
            mydb.commit()
            print(f"Seat {seat_id} added to the seat table.")
        except Exception as e:
            print(f"An error occurred while inserting seat {seat_id}: {e}")
            mydb.rollback()
        finally:
            mycursor.close()
            mydb.close()

    def create_booking(self, customer_id=None):
        # Handles the creation of a booking
        # - Retrieves the last customer ID and booking ID
        # - Prompts the user for movie and showtime selections
        # - Displays the available seating chart and handles seat selection
        # - Inserts new seats if they do not exist in the database
        # - Saves the booking to the database if confirmed by the user

        # Step 1: Get customer ID
        """
        - If a customer ID is provided, use that for the booking.
        - Otherwise, create a new customer and retrieve the customer ID.
        """
        if customer_id:
            self.customer_id = customer_id  # Use the provided customer ID
            last_booking_id = self.get_last_booking_id()
            self.booking_id = self.increment_string(last_booking_id)
        else:
            # New registered customer: Get the last booking ID and increment it
            self.customer_id = self.get_last_customer_id()
            last_booking_id = self.get_last_booking_id()
            self.booking_id = self.increment_string(last_booking_id)


        # Step 2: Get available movies and showtimes from the Movie class
        movie_instance = Movie()  # Create an instance of Movie
        showtimes = movie_instance.get_showtimes()  # Fetch showtimes from the database

        # Display available movies and their showtimes
        movie_instance.display_available_movies_with_showtimes()



        # Step 4: Prompt user to enter movie ID and showtime ID, with validation loop
        while True:
            try:
                my_movie_id = input("\nEnter movie ID: ").strip()
                my_showtime_id = input("Enter showtime ID: ").strip().upper()

                # Validate if the provided movie ID is a number
                if not my_movie_id.isdigit():
                    print("Invalid movie ID. Please enter a numeric value.")
                    continue

                # Look for a matching showtime
                selected_showtime = next(
                    (item for item in showtimes if
                     item['showtime_id'] == my_showtime_id and item.get('movie_id') == int(my_movie_id)),
                    None
                )

                # Retrieve theatre ID based on the selected showtime ID
                # Assuming showtimes is a flat list of dictionaries
                if selected_showtime:
                    self.theatre_id = selected_showtime['theatre_id']
                    self.movie_id = my_movie_id
                    self.showtime_id = my_showtime_id
                    break  # Valid input found, exit loop
                else:
                    print(
                        f"No valid showtime found for Movie ID: {my_movie_id} and Showtime ID: {my_showtime_id}. Please try again.\n")

            except Exception as e:
                print(f"An error occurred: {e}. Please try again.\n")

        # Step 5: Display the seating chart using Theatre class method
        # Load the theatre details and select seats
        theatre_instance = Theatre()
        if not theatre_instance.load_from_db(self.theatre_id):
            print("Failed to load theatre details.")
            return

        seat_instance = Seat(theatre_instance)
        seat_instance.select_seat(my_showtime_id)  # Pass the correct showtime ID

        # Step 6: Check if each selected seat exists and insert if not
        for seat_id in seat_instance.selected_seats:
            if not self.seat_exists(seat_id):
                self.insert_seat(seat_id, self.theatre_id)

        # Step 7: Confirm booking
        print("\nSelected seats:", ", ".join(seat_instance.selected_seats))
        proceed = input("Proceed to checkout? (1 for Yes, 0 for No): ")
        if proceed == '1':
            self.booked_seat = ', '.join(seat_instance.selected_seats)
            self.status = "Confirmed"

            # Save booking to database and get the saved booking_id
            booking_id = self.save_to_db()
            if booking_id:
                booking_details = self.get_booking_details(booking_id)  # Fetch details of this specific booking
                self.print_ticket(booking_details)  # Print ticket with fetched details
            else:
                print("Failed to save booking.")

        else:
            print("Booking cancelled.")
            if seat_instance.selected_seats:
                self.booked_seat = ', '.join(seat_instance.selected_seats)
                self.status = "Cancelled"
                booking_id = self.save_to_db()
                if booking_id:
                    print(f"Booking {booking_id} saved with status 'Cancelled'.")
                else:
                    print("Failed to save cancelled booking.")
            else:
                print("No seat was selected, cancelled booking will not be saved.")

    def save_to_db(self):
        # Saves the current booking details to the database and returns the booking ID.
        mydb = get_db_connection()
        if mydb is None:
            print("Failed to connect to the database.")
            return

        try:
            mycursor = mydb.cursor()
            insert_query = """INSERT INTO booking (booking_id, customer_id, showtime_id, movie_id, theatre_id, booked_seat, status)
                              VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (
                self.booking_id, self.customer_id, self.showtime_id, self.movie_id, self.theatre_id, self.booked_seat,
                self.status)
            mycursor.execute(insert_query, values)
            mydb.commit()
            print(f"\nBooking {self.booking_id} saved successfully.\n")
            return self.booking_id  # Return the booking ID

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            mycursor.close()
            mydb.close()

    def get_booking_details(self, booking_id = None):
        # Retrieves booking details from the database based on booking ID.

        # Use centralized db connection from get_db_connection()
        mydb = get_db_connection()
        if mydb is None:
            print("Failed to connect to the database.")
            return False

        try:
            mycursor = mydb.cursor(dictionary=True)

            # SQL query to retrieve booking + name + price
            select = """
                    SELECT booking.booking_id, customer.customer_id, customer.name,  movie.title, show_time.theatre_id, 
                    show_time.start_time, show_time.show_date, booking.booked_seat, booking.total_price, booking.status
                    FROM booking
                    JOIN movie ON booking.movie_id = movie.movie_id
                    -- since showtime has composite primary key
                    JOIN show_time ON booking.showtime_id = show_time.showtime_id AND booking.movie_id = show_time.movie_id  
                    JOIN customer ON booking.customer_id = customer.customer_id 
                    """

            # Add a WHERE clause if a specific booking_id is provided
            if booking_id:
                select += " WHERE booking.booking_id = %s"
                mycursor.execute(select, (booking_id,))
            else:
                mycursor.execute(select)

            results = mycursor.fetchall()

            # If valid records are found, process and display them
            if results:
                bookings = []
                for result in results:
                    booking_record = {
                        "booking_id": result["booking_id"],
                        "customer_id": result["customer_id"],
                        "name": result["name"],
                        "title": result["title"],
                        "theatre_id": result["theatre_id"],
                        "booked_seat": result["booked_seat"],
                        "start_time": result["start_time"],
                        "show_date": result["show_date"],
                        "total_price": result["total_price"],
                        "status": result["status"]
                    }
                    bookings.append(booking_record)

                return bookings  # Return the list of booking records
            else:
                print("No bookings found.")
                return []

        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            mycursor.close()
            mydb.close()

    def print_ticket(self, booking_details):
        """Prints the ticket details for the latest booking."""
        if booking_details:
            ticket = booking_details[0]  # Only the first result since it's filtered by booking_id
            print("========== TICKET ==========")
            print(f"Booking ID: {ticket['booking_id']}")
            print(f"Customer ID: {ticket['customer_id']}")
            print(f"Customer Name: {ticket['name']}")
            print(f"Movie Title: {ticket['title']}")
            print(f"Theatre ID: {ticket['theatre_id']}")
            print(f"Booked Seat: {ticket['booked_seat']}")
            print(f"Show Date: {ticket['show_date']}")
            print(f"Start Time: {ticket['start_time']}")
            print(f"Total Price: {ticket['total_price']}")
            print(f"Status: {ticket['status']}")
            print("============================")
        else:
            print("Ticket details not found.")
