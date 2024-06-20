import string

# Define the rows and their ranges
rows = 8
row_ranges = {
    'A': 10,
    'B': 10,
    'C': 12,
    'D': 14,
    'E': 14,
    'F': 14,
    'G': 16,
    'H': 16
}

print("             ====================================================")
print("                                   SCREEN")
print("             ====================================================")

# Determine the maximum number of seats in any row
max_range = max(row_ranges.values())

# seat letter - row label
seat = string.ascii_uppercase


def print_seat_numbers(rows, row_ranges, max_range, selected_seats=None):
    if selected_seats is None:
        selected_seats = []

    for i in range(rows):
        row_letter = seat[i]

        # Get number of seats in the current row
        num_seats = row_ranges[row_letter]

        # Generate seat number using
        # temporary variable to store the seat numbers for the current row being processed.
        seats = [f"{row_letter}{j}" for j in range(1, num_seats + 1)]

        # Mark the selected seats with *
        for selected_seat in selected_seats:
            if selected_seat in seats:
                seats[seats.index(selected_seat)] = "**"

        # Create a single string of seat numbers separated by spaces
        seat_row = '  '.join(seats)

        # total width(elements) of the seat row to determine padding to center row
        seat_row_width = len(seat_row)

        # Calculate padding to center the seat row
        padding = (max_range * 5 - seat_row_width) // 2

        print(' ' * padding + seat_row)


def main():
    # List to keep track of all selected seats
    selected_seats = []

    # Initial seat chart display
    print_seat_numbers(rows, row_ranges, max_range, selected_seats)

    while True:
        # Prompt user to select a seat
        selected_seat = input("\nSelect a seat (e.g., A1) or type 'exit' to quit: ").strip().upper()

        if selected_seat.lower() == 'exit':
            break

        # Validate the selected seat
        row = selected_seat[0] if len(selected_seat) > 0 else ''
        number = selected_seat[1:] if len(selected_seat) > 1 else ''


        if row in row_ranges and number.isdigit() and 1 <= int(number) <= row_ranges[row]:
            if selected_seat not in selected_seats:
                # Add the valid and new seat to the list of selected seats
                selected_seats.append(selected_seat)

                # Clear the console
                print("\n" * 7)

                # Reprint the seating chart with all selected seats marked
                print("             ====================================================")
                print("                                   SCREEN")
                print("             ====================================================")
                print_seat_numbers(rows, row_ranges, max_range, selected_seats)
            else:
                print("Seat already selected. Choose a different seat.")
        else:
            print("Invalid seat number. Please try again.")


main()
