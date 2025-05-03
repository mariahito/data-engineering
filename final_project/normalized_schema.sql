
-- Table 1: states
CREATE TABLE states (
    state_id SERIAL PRIMARY KEY,
    state_name VARCHAR(50) UNIQUE NOT NULL,
    fips_code INT UNIQUE
);

-- Table 2: time
CREATE TABLE time (
    time_id SERIAL PRIMARY KEY,
    month_year VARCHAR(10) UNIQUE NOT NULL
);

-- Table 3: weather
CREATE TABLE weather (
    weather_id SERIAL PRIMARY KEY,
    state_id INT REFERENCES states(state_id),
    time_id INT REFERENCES time(time_id),
    temp_max FLOAT,
    temp FLOAT,
    temp_min FLOAT,
    feels_like FLOAT,
    humidity FLOAT,
    precipitation FLOAT,
    precipitation_type VARCHAR(50),
    conditions VARCHAR(100)
);

-- Table 4: employment
CREATE TABLE employment (
    employment_id SERIAL PRIMARY KEY,
    state_id INT REFERENCES states(state_id),
    time_id INT REFERENCES time(time_id),
    civilian_population INT,
    labor_force INT,
    population_percent FLOAT,
    employment INT,
    employment_percent FLOAT,
    unemployment INT,
    unemployment_percent FLOAT,
    employment_to_population_ratio FLOAT,
    unemployment_rate FLOAT
);
