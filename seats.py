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


def print_seat_numbers(rows, row_ranges, max_range):
    for i in range(rows):
        row_letter = seat[i]

        # Get number of seats in the current row
        num_seats = row_ranges[row_letter]

        # Generate seat number
        seats = [f"{row_letter}{i}" for i in range(1, num_seats + 1)]

        # Create a single string of seat numbers separated by spaces
        seat_row = '  '.join(seats)

        # Calculate the total width of the seat row
        seat_row_width = len(seat_row)

        # Calculate padding to center the seat row
        padding = (max_range * 5 - seat_row_width) // 2  # Each seat takes about 3 characters (e.g., "A1 ")

        # Print the centered seat row
        print(' ' * padding + seat_row)


print_seat_numbers(rows, row_ranges, max_range)
