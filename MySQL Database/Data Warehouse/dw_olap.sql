USE tb_data_warehouse;




-- QUERIES

-- Revenue by Theatre:
SELECT dim_theatre.theatre_id AS Theatre,
SUM(fact_booking.total_price) AS Total_Revenue
FROM fact_booking
JOIN dim_theatre ON fact_booking.theatre_id = dim_theatre.theatre_id
GROUP BY dim_theatre.theatre_id
ORDER BY Total_Revenue DESC;


-- Regional Trends in Bookings
SELECT fact_booking.theatre_id AS Theatre,
COUNT(fact_booking.theatre_id) AS  Total_Bookings,
SUM(fact_booking.total_price) AS Total_Revenue
FROM fact_booking
GROUP BY fact_booking.theatre_id
ORDER BY Theatre ASC;



-- Student Discounts Usage: Analyze how many students book tickets to see if the discount is effective.
SELECT dim_customer.student, 
count(fact_booking.booking_id) as bookings,
round(((count(fact_booking.booking_id) / (SELECT COUNT(*) FROM fact_booking)) * 100), 1) as percentage_bookings
FROM fact_booking
JOIN dim_customer ON fact_booking.customer_id = dim_customer.customer_id
GROUP BY dim_customer.student;

-- Compare Revenue Between Student and Non-Student
SELECT dim_customer.student,
COUNT(fact_booking.booking_id) AS Total_Bookings,
SUM(fact_booking.total_price) AS Total_Revenue
FROM fact_booking
JOIN dim_customer ON fact_booking.customer_id = dim_customer.customer_id
GROUP BY dim_customer.student
ORDER BY Total_Revenue DESC;

-- Repeat Customers: Identify loyal customers by counting how many times each customer books.
SELECT dim_customer.name, COUNT(fact_booking.booking_id) AS bookings
FROM fact_booking 
JOIN dim_customer ON fact_booking.customer_id = dim_customer.customer_id
GROUP BY dim_customer.name
HAVING bookings > 1
ORDER BY bookings DESC;

-- Most Booked Movies: Identify top-performing movies to inform future selections
SELECT dim_movie.title, COUNT(fact_booking.booking_id) AS bookings
FROM fact_booking 
JOIN dim_movie  ON fact_booking.movie_id = dim_movie.movie_id
GROUP BY dim_movie.title
ORDER BY bookings DESC;


-- Movie revenue
SELECT dim_movie.title AS Movie,
SUM(fact_booking.total_price) AS Total_Revenue
FROM fact_booking 
JOIN dim_movie ON fact_booking.movie_id = dim_movie.movie_id
GROUP BY dim_movie.movie_id
ORDER BY Total_Revenue ASC;

-- Seat Utilization: Determine which rows are most popular.
SELECT LEFT(fact_booking.booked_seat, 1) AS Row_Letter,
COUNT(fact_booking.booking_id) AS Total_Bookings
FROM fact_booking 
GROUP BY Row_Letter
ORDER BY Row_Letter ASC;

