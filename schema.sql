CREATE TABLE airplane_crashes (
    id SERIAL PRIMARY KEY,
    event_date DATE NOT NULL,
    location VARCHAR(255),
    operator VARCHAR(255),
    aircraft_type VARCHAR(255),
    registration VARCHAR(50),
    flight_number VARCHAR(50),
    route VARCHAR(255),
    fatalities INTEGER,
    description TEXT,
    source_url VARCHAR(255)
);
