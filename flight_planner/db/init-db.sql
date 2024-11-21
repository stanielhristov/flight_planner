CREATE TABLE IF NOT EXISTS cities
(
    id        SERIAL PRIMARY KEY,
    city_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS airports
(
    id      SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL REFERENCES cities (id),
    name    TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS flights
(
    flight_id            SERIAL PRIMARY KEY,
    departure_airport_id INTEGER        NOT NULL REFERENCES airports (id) ON DELETE CASCADE,
    arrival_airport_id   INTEGER        NOT NULL REFERENCES airports (id) ON DELETE CASCADE,
    departure_time       TIMESTAMP      NOT NULL,
    travel_time          INTEGER        NOT NULL CHECK (travel_time > 0),
    price                NUMERIC(10, 2) NOT NULL CHECK (price >= 0)
);

INSERT INTO public.cities (city_name)
VALUES ('New York')
ON CONFLICT DO NOTHING;
INSERT INTO public.cities (city_name)
VALUES ('Los Angeles')
ON CONFLICT DO NOTHING;
INSERT INTO public.cities (city_name)
VALUES ('Chicago')
ON CONFLICT DO NOTHING;
INSERT INTO public.cities (city_name)
VALUES ('Houston')
ON CONFLICT DO NOTHING;
INSERT INTO public.cities (city_name)
VALUES ('Phoenix')
ON CONFLICT DO NOTHING;
INSERT INTO public.cities (city_name)
VALUES ('Philadelphia')
ON CONFLICT DO NOTHING;
INSERT INTO public.cities (city_name)
VALUES ('San Antonio')
ON CONFLICT DO NOTHING;
INSERT INTO public.cities (city_name)
VALUES ('San Diego')
ON CONFLICT DO NOTHING;
INSERT INTO public.cities (city_name)
VALUES ('Dallas')
ON CONFLICT DO NOTHING;
INSERT INTO public.cities (city_name)
VALUES ('San Jose')
ON CONFLICT DO NOTHING;

INSERT INTO public.airports (city_id, name)
VALUES (1, 'John F. Kennedy International Airport')
ON CONFLICT DO NOTHING;
INSERT INTO public.airports (city_id, name)
VALUES (1, 'LaGuardia Airport')
ON CONFLICT DO NOTHING;
INSERT INTO public.airports (city_id, name)
VALUES (2, 'Los Angeles International Airport')
ON CONFLICT DO NOTHING;
INSERT INTO public.airports (city_id, name)
VALUES (2, 'Bob Hope Airport')
ON CONFLICT DO NOTHING;
INSERT INTO public.airports (city_id, name)
VALUES (3, 'Hare International Airport')
ON CONFLICT DO NOTHING;
INSERT INTO public.airports (city_id, name)
VALUES (3, 'Midway International Airport')
ON CONFLICT DO NOTHING;
INSERT INTO public.airports (city_id, name)
VALUES (4, 'George Bush Intercontinental Airport')
ON CONFLICT DO NOTHING;
INSERT INTO public.airports (city_id, name)
VALUES (4, 'William P. Hobby Airport')
ON CONFLICT DO NOTHING;
INSERT INTO public.airports (city_id, name)
VALUES (5, 'Phoenix Sky Harbor International Airport')
ON CONFLICT DO NOTHING;
INSERT INTO public.airports (city_id, name)
VALUES (5, 'Phoenix-Mesa Gateway Airport')
ON CONFLICT DO NOTHING;

INSERT INTO public.flights (departure_airport_id, arrival_airport_id, departure_time, travel_time, price)
VALUES (1, 2, '2024-12-01 08:00', 180, 250.00)
ON CONFLICT DO NOTHING;

INSERT INTO public.flights (departure_airport_id, arrival_airport_id, departure_time, travel_time, price)
VALUES (2, 3, '2024-12-01 09:00', 210, 300.00)
ON CONFLICT DO NOTHING;

INSERT INTO public.flights (departure_airport_id, arrival_airport_id, departure_time, travel_time, price)
VALUES (3, 4, '2024-12-01 10:00', 150, 200.00)
ON CONFLICT DO NOTHING;

INSERT INTO public.flights (departure_airport_id, arrival_airport_id, departure_time, travel_time, price)
VALUES (4, 5, '2024-12-01 11:00', 240, 350.00)
ON CONFLICT DO NOTHING;

INSERT INTO public.flights (departure_airport_id, arrival_airport_id, departure_time, travel_time, price)
VALUES (5, 6, '2024-12-01 12:00', 180, 275.00)
ON CONFLICT DO NOTHING;

INSERT INTO public.flights (departure_airport_id, arrival_airport_id, departure_time, travel_time, price)
VALUES (6, 7, '2024-12-01 13:00', 200, 220.00)
ON CONFLICT DO NOTHING;

INSERT INTO public.flights (departure_airport_id, arrival_airport_id, departure_time, travel_time, price)
VALUES (7, 8, '2024-12-01 14:00', 220, 300.00)
ON CONFLICT DO NOTHING;

INSERT INTO public.flights (departure_airport_id, arrival_airport_id, departure_time, travel_time, price)
VALUES (8, 9, '2024-12-01 15:00', 160, 180.00)
ON CONFLICT DO NOTHING;

INSERT INTO public.flights (departure_airport_id, arrival_airport_id, departure_time, travel_time, price)
VALUES (9, 10, '2024-12-01 16:00', 190, 260.00)
ON CONFLICT DO NOTHING;

INSERT INTO public.flights (departure_airport_id, arrival_airport_id, departure_time, travel_time, price)
VALUES (10, 1, '2024-12-01 17:00', 200, 230.00)
ON CONFLICT DO NOTHING;