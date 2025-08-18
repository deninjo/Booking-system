USE tb_data_warehouse;

--  Automate the ETL Process Using  MySQL scheduled events


-- Drop events first to avoid duplicates
DROP EVENT IF EXISTS load_customer_data;
DROP EVENT IF EXISTS load_movie_data;
DROP EVENT IF EXISTS load_showtime_data;
DROP EVENT IF EXISTS load_theatre_data;
DROP EVENT IF EXISTS load_fact_booking;

-- 1. Customer Dimension
DELIMITER //
CREATE EVENT load_customer_data
ON SCHEDULE EVERY 7 DAY
STARTS CURRENT_TIMESTAMP
DO
BEGIN
    INSERT IGNORE INTO dim_customer (customer_id, name, phone_number, student)
    SELECT customer_id, name, phone_number, student
    FROM ticket_booking.customer
    WHERE customer_id NOT IN (SELECT customer_id FROM dim_customer);
END //
DELIMITER ;

-- 2. Movie Dimension
DELIMITER //
CREATE EVENT load_movie_data
ON SCHEDULE EVERY 7 DAY
STARTS CURRENT_TIMESTAMP
DO
BEGIN
    INSERT IGNORE INTO dim_movie (movie_id, title, IMDB)
    SELECT movie_id, title, IMDB
    FROM ticket_booking.movie
    WHERE movie_id NOT IN (SELECT movie_id FROM dim_movie);
END //
DELIMITER ;

-- 3. Showtime Dimension
DELIMITER //
CREATE EVENT load_showtime_data
ON SCHEDULE EVERY 7 DAY
STARTS CURRENT_TIMESTAMP
DO
BEGIN
    INSERT IGNORE INTO dim_showtime (showtime_id, movie_id, theatre_id, show_date, start_time)
    SELECT showtime_id, movie_id, theatre_id, show_date, start_time
    FROM ticket_booking.show_time
    WHERE showtime_id NOT IN (SELECT showtime_id FROM dim_showtime);
END //
DELIMITER ;

-- 4. Theatre Dimension
DELIMITER //
CREATE EVENT load_theatre_data
ON SCHEDULE EVERY 7 DAY
STARTS CURRENT_TIMESTAMP
DO
BEGIN
    INSERT IGNORE INTO dim_theatre (theatre_id, screen, layout)
    SELECT theatre_id, screen, layout
    FROM ticket_booking.theatre
    WHERE theatre_id NOT IN (SELECT theatre_id FROM dim_theatre);
END //
DELIMITER ;

-- 5. Fact Booking Table (only confirmed bookings in the last 7 days)
DELIMITER //
CREATE EVENT load_fact_booking
ON SCHEDULE EVERY 7 DAY
STARTS CURRENT_TIMESTAMP
DO
BEGIN
    INSERT IGNORE INTO fact_booking (
        booking_id, customer_id, movie_id, showtime_id, theatre_id,
        booked_seat, total_price, booking_date
    )
    SELECT 
        booking_id,
        customer_id,
        movie_id,
        showtime_id,
        theatre_id,
        booked_seat,
        total_price,
        booking_date 
    FROM ticket_booking.booking 
    WHERE status = 'Confirmed'
      AND booking_date >= CURDATE() - INTERVAL 7 DAY
      AND booking_id NOT IN (SELECT booking_id FROM fact_booking);
END //
DELIMITER ;
