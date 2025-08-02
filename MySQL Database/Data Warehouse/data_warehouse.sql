DROP DATABASE IF EXISTS tb_data_warehouse;
CREATE DATABASE tb_data_warehouse;

-- Switch to the new data warehouse database
USE tb_data_warehouse;


-- Dimension Tables
-- 1. Customer Dimension
CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    phone_number VARCHAR(10),
    student BOOLEAN
);

-- 2. Movie Dimension
CREATE TABLE dim_movie (
    movie_id INT PRIMARY KEY,
    title VARCHAR(45),
    IMDB DECIMAL(2,1)
);


-- 3. Showtime Dimension
CREATE TABLE dim_showtime (
    showtime_id VARCHAR(5) ,
    movie_id INT ,
    theatre_id VARCHAR(4),
    show_date DATE,
    start_time TIME,
    PRIMARY KEY (showtime_id, movie_id, theatre_id)
);

-- 4. Theatre Dimension
CREATE TABLE dim_theatre (
    theatre_id VARCHAR(4) PRIMARY KEY,
    screen VARCHAR(100),
    layout VARCHAR(100)
);

-- Fact Table
CREATE TABLE fact_booking (
    booking_id VARCHAR(5) PRIMARY KEY,
    customer_id INT,
    movie_id INT,
    showtime_id VARCHAR(5),
    theatre_id VARCHAR(4),
    booked_seat VARCHAR(20),
    total_price DECIMAL(10, 2),
    booking_date DATE,
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (movie_id) REFERENCES dim_movie(movie_id),
    FOREIGN KEY (showtime_id) REFERENCES dim_showtime(showtime_id),
    FOREIGN KEY (theatre_id) REFERENCES dim_theatre(theatre_id)
);
