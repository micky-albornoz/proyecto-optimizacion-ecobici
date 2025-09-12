-- Esquema SQL para la base de datos de Ecobici

-- Borra las tablas si ya existen para permitir una recarga limpia
DROP TABLE IF EXISTS fact_trips;
DROP TABLE IF EXISTS dim_stations;

-- Tabla de Dimension: Estaciones
CREATE TABLE dim_stations (
    station_id INT PRIMARY KEY,
    station_name VARCHAR(255),
    latitude REAL,
    longitude REAL
);

-- Tabla de Hechos: Viajes
CREATE TABLE fact_trips (
    trip_id SERIAL PRIMARY KEY,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration_minutes INT,
    start_station_id INT REFERENCES dim_stations(station_id),
    end_station_id INT REFERENCES dim_stations(station_id)
);