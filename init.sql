CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(20) NOT NULL,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    battery FLOAT NOT NULL,
    status VARCHAR(10) NOT NULL,
    region VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP NOT NULL
);
