DROP DATABASE IF EXISTS ticket_booking;
CREATE DATABASE ticket_booking;
USE ticket_booking;


-- creating tables
CREATE TABLE customer(
    customer_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    email VARCHAR(30) NOT NULL UNIQUE,
    phone_number VARCHAR(10) NOT NULL UNIQUE,
    student TINYINT(1) NOT NULL CHECK (student IN (0, 1)), -- Only allows 0 or 1
    password VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_id)
);
DROP TABLE customer;

CREATE TABLE movie(
	movie_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(45) NOT NULL,
    genre VARCHAR(30) NOT NULL,
    rating VARCHAR(10) NOT NULL,
    IMDB DECIMAL(2,1) NOT NULL,
    duration INT NOT NULL,
    year_of_release YEAR NOT NULL,
    PRIMARY KEY(movie_id)
);
DROP TABLE movie;

CREATE TABLE theatre(
	theatre_id VARCHAR(4) NOT NULL,
    screen VARCHAR(2) NOT NULL,
    layout VARCHAR(100) NOT NULL,
    PRIMARY KEY(theatre_id)
);
DROP TABLE theatre;

CREATE TABLE show_time(
	showtime_id VARCHAR(5) NOT NULL,
    movie_id INT NOT NULL,
    theatre_id VARCHAR(4) NOT NULL,
    show_date DATE NOT NULL,
    start_time TIME NOT NULL,
    PRIMARY KEY(showtime_id, movie_id),
    FOREIGN KEY(movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    FOREIGN KEY(theatre_id) REFERENCES theatre(theatre_id) ON DELETE CASCADE
);
DROP TABLE show_time;

CREATE TABLE seat(
	seat_id VARCHAR(4) NOT NULL,
    theatre_id VARCHAR(4) NOT NULL,
    row_letter VARCHAR(1) NOT NULL,
    number INT NOT NULL,
    PRIMARY KEY(seat_id, theatre_id),
    FOREIGN KEY(theatre_id) REFERENCES theatre(theatre_id) ON DELETE CASCADE
);
ALTER TABLE seat
MODIFY seat_id VARCHAR(4) NOT NULL;

DROP TABLE seat;

CREATE TABLE price(
	price_id VARCHAR(10) NOT NULL,
    showtime_id VARCHAR(5) NOT NULL,
    seat_category VARCHAR(15) NOT NULL,
    price DECIMAL(5,2) NOT NULL,
    PRIMARY KEY(price_id),
    FOREIGN KEY(showtime_id) REFERENCES show_time(showtime_id) ON DELETE CASCADE
);
DROP TABLE price;


CREATE TABLE booking(
    booking_id VARCHAR(5) NOT NULL,
    customer_id INT NOT NULL,
    showtime_id VARCHAR(5) NOT NULL,
    theatre_id VARCHAR(4) NOT NULL,
    booked_seat VARCHAR(4) NOT NULL,
    total_price DECIMAL(5,2) NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL,
    PRIMARY KEY(booking_id),
    FOREIGN KEY(customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY(showtime_id) REFERENCES show_time(showtime_id) ON DELETE CASCADE,
    FOREIGN KEY (theatre_id) REFERENCES theatre(theatre_id) ON DELETE CASCADE,
    FOREIGN KEY(booked_seat) REFERENCES seat(seat_id) ON DELETE CASCADE
);

ALTER TABLE booking
ADD theatre_id VARCHAR(4) NULL AFTER showtime_id,
ADD CONSTRAINT fk_theatre
    FOREIGN KEY (theatre_id) REFERENCES theatre(theatre_id)
    ON DELETE SET NULL;
    
ALTER TABLE booking
MODIFY booked_seat VARCHAR(4) NOT NULL;

DROP TABLE booking;


-- Debugging Table for booking table
CREATE TEMPORARY TABLE IF NOT EXISTS debug_log (
    log_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    message TEXT
);

TRUNCATE TABLE debug_log; -- clears records
SELECT * FROM debug_log;


-- inserting values to customer table
INSERT INTO customer(customer_id, name, email, phone_number, student, password)
VALUES
(101, "Kaskazini McOure", 'kaskazini@gmail.com', '0712345678', 0, 'xxxxx');

INSERT INTO customer(name, email, phone_number, student, password)	
VALUES 
("Alladin's Carpet", 'magic77@gmail.com', '0787654321', 1, 'xxx');

INSERT INTO customer(name, email, phone_number, student, password)	
VALUES 
("Jesse Pinkman", 'chillipowder@gmail.com', '0787677021', 1, 'xxxx');

INSERT INTO customer(name, email, phone_number, student, password)	
VALUES 
("Eren Jaegar", 'titanslayer@gmail.com', '0752677021', 0, 'xxxx');

SELECT * FROM customer;
UPDATE customer
SET customer_id = 104
WHERE customer_id = 105;


-- inserting values to movie table
INSERT INTO movie
VALUES (701, 'Pulp Fiction', 'Drug Crime', 'R', 8.9, 154, 1994);
INSERT INTO movie(title, genre, rating, IMDB, duration, year_of_release)
VALUES ('V for Vendetta', 'Political Thriller', 'R', 8.1, 132, 2005);
INSERT INTO movie(title, genre, rating, IMDB, duration, year_of_release)
VALUES ('Reservoir Dogs', 'Crime', 'R', 8.3, 99, 1992);
INSERT INTO movie(title, genre, rating, IMDB, duration, year_of_release)
VALUES ('The Prestige', 'Mystery', 'PG-13', 8.5, 130, 2006);

SELECT * FROM movie;


-- inserting values to theatre table
INSERT INTO theatre
VALUES ('IA', '2D', "'A': 10, 'B': 10, 'C': 12, 'D': 14, 'E': 14, 'F': 14, 'G': 16, 'H': 16");
INSERT INTO theatre
VALUES ('IB', '3D', "'A': 10, 'B': 10, 'C': 12, 'D': 14, 'E': 14, 'F': 14, 'G': 16");
INSERT INTO theatre
VALUES ('IIA', '2D', "'A': 12, 'B': 12, 'C': 12, 'D': 14, 'E': 14, 'F': 14, 'G': 16, 'H': 16");
INSERT INTO theatre
VALUES ('IIB', '3D', "'A': 12, 'B': 12, 'C': 12, 'D': 14, 'E': 14, 'F': 14, 'G': 16");

DELETE FROM theatre
where theatre_id = 'IIB';
SELECT * FROM theatre;


-- inserting values to show_time
INSERT INTO show_time
VALUES
('WD-M', 701, 'IIB', '2024-9-11', '10:45:00');

SELECT * FROM show_time;


-- inserting values to price table
INSERT INTO price
VALUES ('P01', 'WD-M', 'Front', 450.00);
INSERT INTO price
VALUES ('P02', 'WD-M', 'Executive', 450.00);
INSERT INTO price
VALUES ('P03', 'WD-M', 'Rear', 450.00);

INSERT INTO price
VALUES ('P04', 'WD-A', 'Front', 550.00);
INSERT INTO price
VALUES ('P05', 'WD-A', 'Executive', 550.00);
INSERT INTO price
VALUES ('P06', 'WD-A', 'Rear', 650.00);

INSERT INTO price
VALUES ('P07', 'WD-N', 'Front', 650.00);
INSERT INTO price
VALUES ('P08', 'WD-N', 'Executive', 650.00);
INSERT INTO price
VALUES ('P09', 'WD-N', 'Rear', 750.00);

INSERT INTO price
VALUES ('P10', 'WE-A', 'Front', 600.00);
INSERT INTO price
VALUES ('P11', 'WE-A', 'Executive', 600.00);
INSERT INTO price
VALUES ('P12', 'WE-A', 'Rear', 700.00);

INSERT INTO price
VALUES ('P13', 'WE-N', 'Front', 750.00);
INSERT INTO price
VALUES ('P14', 'WE-N', 'Executive', 750.00);
INSERT INTO price
VALUES ('P15', 'WE-N', 'Rear', 850.00);

SELECT * FROM price ORDER BY price_id ASC;
DELETE FROM price WHERE price_id = 'P9';


-- inserting values to seat table 
INSERT INTO seat VALUES ('A1', 'IA', 'A', 1);
INSERT INTO seat VALUES ('E5', 'IIB', 'E', 5);
INSERT INTO seat VALUES ('H12', 'IA', 'H', 12);


-- inserting values to booking table
INSERT INTO booking(booking_id, customer_id, showtime_id, theatre_id, booked_seat, status)
VALUES('B001', 101, 'WE-N','IA', 'H12', 'Confirmed');

INSERT INTO booking(booking_id, customer_id, showtime_id, theatre_id, booked_seat, status)
VALUES('B002', 103, 'WD-A','IIA', 'E5', 'Cancelled');

INSERT INTO booking(booking_id, customer_id, showtime_id, theatre_id, booked_seat, status)
VALUES('B003', 102, 'WD-M','IA', 'H12', 'Confirmed');


DELETE FROM booking where booking_id = 'B007';
SELECT * FROM booking;

ALTER TABLE ticket_booking.customer AUTO_INCREMENT = 105;




-- showtimes for movies
SELECT show_time.showtime_id, movie.title, theatre.screen, show_time.start_time, show_time.show_date
FROM show_time
JOIN movie ON show_time.movie_id = movie.movie_id
JOIN theatre ON show_time.theatre_id = theatre.theatre_id;

-- showtime for specific movie
SELECT show_time.showtime_id, movie.title, show_time.start_time, show_time.show_date
FROM show_time
JOIN movie
ON show_time.movie_id = movie.movie_id
WHERE movie.title = 'Pulp Fiction';

-- showtime + screen type
SELECT show_time.showtime_id, movie.title, theatre.screen, show_time.start_time, show_time.show_date
FROM show_time
JOIN movie ON show_time.movie_id = movie.movie_id
JOIN theatre ON show_time.theatre_id = theatre.theatre_id
WHERE movie.title = 'Pulp Fiction';










