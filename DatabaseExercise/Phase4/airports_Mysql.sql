CREATE TABLE airports(
	code VARCHAR(3) NOT NULL,
	lat DECIMAL(10,8) NOT NULL,
	lon DECIMAL(11,8) NOT NULL,
	name VARCHAR(255) NOT NULL,
	city VARCHAR(255) NOT NULL,
	state VARCHAR(255) NOT NULL,
	country VARCHAR(255) NOT NULL,
	woeid INT(11) NOT NULL,
	tz VARCHAR(255),
	phone VARCHAR(20),
	type VARCHAR(50),
	email VARCHAR(255),
	url VARCHAR(2083),
	runway_length INT(11),
	elev INT(11),
	icao VARCHAR(255),
	direct_flights INT,
	carriers INT
	
);

LOAD DATA INFILE  '/$PATH/airports.CSV' INTO TABLE airports;

SELECT * FROM airports WHERE country = 'United States';

SELECT * FROM airports WHERE country = 'United States' GROUP BY city;

SELECT * FROM airports WHERE country = 'United States' AND city = 'Boston';

UPDATE airports SET city = 'Boston_updated' WHERE code = 'BOS';

SELECT * FROM airports WHERE country = 'United States' and city = 'Boston_updated';

