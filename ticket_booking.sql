DROP DATABASE IF EXISTS ticket_booking;
CREATE DATABASE ticket_booking;

USE ticket_booking;

CREATE TABLE customer_details(
	id INTEGER AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    email VARCHAR(30) NOT NULL UNIQUE,
    phone_number VARCHAR(10) NOT NULL UNIQUE,
    student TINYINT(1),
    PRIMARY KEY(id)
);

DROP TABLE customer_details;


INSERT INTO customer_details
VALUES
(1, "Kaskazini McOure", 'kaskazini@gmail.com', '0712345678', 0);



DELETE FROM customer_details
WHERE id = 1;
	
