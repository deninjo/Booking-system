DROP DATABASE IF EXISTS ticket_booking;
CREATE DATABASE ticket_booking;
USE ticket_booking;


-- creating tables
CREATE TABLE customer_details(
	customer_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    email VARCHAR(30) NOT NULL UNIQUE,
    phone_number VARCHAR(10) NOT NULL UNIQUE,
    student TINYINT(1) NOT NULL,
    password VARCHAR(50) ,
    PRIMARY KEY(customer_id)
);
DROP TABLE customer_details;

CREATE TABLE movies(
	movie_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(25) NOT NULL,
    genre VARCHAR(10) NOT NULL,
    rating VARCHAR(10) NOT NULL,
    IMDB DECIMAL(2,1) NOT NULL,
    duration INT NOT NULL,
    year_of_release YEAR NOT NULL,
    PRIMARY KEY(movie_id)
);
DROP TABLE movies;

CREATE TABLE theatre(
	theatre_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    seat_capacity INT NOT NULL,
    layout VARCHAR(100) NOT NULL,
    PRIMARY KEY(theatre_id)
);

CREATE TABLE show_time(
	showtime_id VARCHAR(20) NOT NULL,
    movie_id INT NOT NULL,
    dimension VARCHAR(2) NOT NULL,
    theatre_id INT NOT NULL,
    show_date DATE NOT NULL,
    start_time TIME NOT NULL
);

CREATE TABLE bookings(
	booking_id VARCHAR(20) NOT NULL,
    theatre_id INT NOT NULL,
    showtime_id VARCHAR(20) NOT NULL,
    customer_id INTEGER NOT NULL,
    selected_seats VARCHAR(3) NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE prices(
	price_id VARCHAR(10) NOT NULL,
    showtime_id VARCHAR(20) NOT NULL,
    seat_category VARCHAR(15) NOT NULL,
    price DECIMAL(5,2) NOT NULL
);

    
-- inserting values to tables
INSERT INTO customer_details
VALUES
(100, "Kaskazini McOure", 'kaskazini@gmail.com', '0712345678', 0, 'fmdffnfn');

INSERT INTO customer_details
	(name, email, phone_number, student, password)
VALUES 
("Nane Nane", 'nanenane@gmail.com', '0787654321', 1, 'knsvkl');



INSERT INTO movies
VALUES
(700, 'Pulp Fiction', 'Drug Crime', 'R', 8.9, 154, 1994);
	
