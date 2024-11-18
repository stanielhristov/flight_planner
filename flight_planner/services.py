from connection import get_connection
from datetime import datetime
from entities import Flight
from storage import CityStorage
from storage import AirportStorage


class CityService:
    """ A bunch of @staticmethod's """

    @classmethod
    def create_city(cls, json):
        name = json['name']

        storage = CityStorage()

        return storage.create(name)

    @classmethod
    def get_all_cities(cls):
        storage = CityStorage()

        return storage.get_all()

    @classmethod
    def get_city(cls, city_id):
        storage = CityStorage()
        city = storage.get(city_id)

        if city is None:
            raise KeyError()

        return city

    @classmethod
    def get_city_by_name(cls, name):
        storage = CityStorage()
        city = storage.get_by_name(name)

        if city is None:
            raise KeyError()

        return city

    @classmethod
    def delete_city(cls, city_id):
        storage = CityStorage()
        storage.delete(city_id)

        return ''

    @classmethod
    def delete_all_cities(cls):
        storage = CityStorage()
        storage.delete_all()

        return ''


class AirportService:
    """ A bunch of @staticmethod's """

    @classmethod
    def create_airport(cls, json):
        name = json['name']
        city = json['city']

        if CityService.get_city(city) is None:
            return {"error": "City not found"}
        else:
            storage = AirportStorage()
            res = storage.create(name, city)
            return res

    @classmethod
    def update_all_airports(cls, json):
        pass

    @classmethod
    def delete_all_airports(cls):
        storage = AirportStorage()
        storage.delete_all()

        return ''

    @classmethod
    def get_all_airports(cls):
        storage = AirportStorage()

        return storage.get_all()


    @classmethod
    def get_airport(cls, airport_id):
        storage = AirportStorage()
        airport = storage.get(airport_id)

        if airport is None:
            raise KeyError()

        return storage.get(airport)

    @classmethod
    def delete_airport(cls, airport_id):
        storage = AirportStorage()
        storage.delete(airport_id)

        return ''

    @classmethod
    def update_airport(cls, airport_id, json):
        connection = get_connection()

        if connection is None:
            return {"error": "Could not establish a database connection"}

        try:
            name = json.get('name')
            city_id = json.get('city_id')

            update_query = "UPDATE airports SET name = %s, city_id = %s WHERE id = %s"
            values = (name, city_id, airport_id)

            with connection.cursor() as cursor:
                cursor.execute(update_query, values)

                rows_updated = cursor.rowcount

                connection.commit()

                if rows_updated > 0:
                    return {"message": f"Airport with ID {airport_id} has been updated successfully"}
                else:
                    return {"error": "Airport not found"}

        except Exception as e:
            connection.rollback()
            return {"error": f"Error updating airport: {str(e)}"}

        finally:
            connection.close()


class FlightService:
    """ A bunch of @staticmethod's """

    @classmethod
    def create_flight(cls, json):

        try:
            departure_airport_id = json["departureAirport"]
            arrival_airport_id = json["arrivalAirport"]
            departure_time = json["departureTime"]
            travel_time = json["travelTime"]
            price_str = json["price"]

            try:
                price = float(price_str.replace('$', ''))
            except ValueError:
                return {
                    "error": f"Invalid price format: {price_str}. Ensure it's a valid number with or without a dollar sign."}

            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM airports WHERE id = %s", (departure_airport_id,))
                departure_airport = cursor.fetchone()

                if not departure_airport:
                    return {"error": f"Departure airport with ID {departure_airport_id} not found"}

                cursor.execute("SELECT id FROM airports WHERE id = %s", (arrival_airport_id,))
                arrival_airport = cursor.fetchone()

                if not arrival_airport:
                    return {"error": f"Arrival airport with ID {arrival_airport_id} not found"}

            flight = Flight(
                departure_airport_id=departure_airport_id,
                arrival_airport_id=arrival_airport_id,
                departure_time=departure_time,
                travel_time=travel_time,
                price=price
            )

            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO flights (departure_airport_id, arrival_airport_id, departure_time, travel_time, price)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (flight.departure_airport_id, flight.arrival_airport_id,
                     flight.departure_time.strftime('%H:%M'), flight.travel_time, flight.price)
                )
                connection.commit()

            return {"message": "Flight created successfully"}

        except Exception as e:
            if 'connection' in locals():
                connection.rollback()
            return {"error": f"Error creating flight: {str(e)}"}
        finally:
            if 'connection' in locals():
                connection.close()

    @classmethod
    def get_all_flights(cls, offset, max_count, sort_by, sort_order):
        connection = get_connection()

        if connection is None:
            return {"error": "Could not establish a database connection"}

        try:
            valid_sort_columns = ['departureTime', 'price', 'travelTime']
            valid_sort_orders = ['ASC', 'DESC']

            if sort_by not in valid_sort_columns:
                return {"error": f"Invalid sort_by field: {sort_by}. Valid options are {valid_sort_columns}."}

            if sort_order not in valid_sort_orders:
                return {"error": f"Invalid sort_order field: {sort_order}. Valid options are {valid_sort_orders}."}

            if sort_by == 'departureTime':
                sort_by = 'departure_time'

            if sort_by == "travelTime":
                sort_by = 'travel_time'

            query = f"""
                        SELECT flights.flight_id, departure_airport_id, arrival_airport_id, departure_time, travel_time, price
                        FROM flights
                        ORDER BY {sort_by} {sort_order}
                        LIMIT %s OFFSET %s
                    """
            with connection.cursor() as cursor:
                cursor.execute(query, (max_count, offset))
                flights = cursor.fetchall()

            flight_list = [
                {
                    "id": flight[0],
                    "departure_airport_id": flight[1],
                    "arrival_airport_id": flight[2],
                    "departure_time": flight[3].strftime('%H:%M') if flight[3] else None,
                    "travel_time": flight[4],
                    "price": flight[5]
                }
                for flight in flights
            ]

            return {"flights": flight_list}

        except Exception as e:
            return {"error": f"Error fetching flights: {str(e)}"}

        finally:
            if 'connection' in locals():
                connection.close()

    @classmethod
    def search_flights(cls, search_criteria):
        connection = get_connection()

        if connection is None:
            return {"error": "Could not establish a database connection"}

        try:
            departure_city = search_criteria.get("departureCity")
            arrival_city = search_criteria.get("arrivalCity")
            min_price = search_criteria.get("minPrice")
            max_price = search_criteria.get("maxPrice")
            min_departure_time = search_criteria.get("minDepartureTime")
            max_departure_time = search_criteria.get("maxDepartureTime")
            max_travel_time = search_criteria.get("maxTravelTime")
            min_arrival_time = search_criteria.get("minArrivalTime")
            max_arrival_time = search_criteria.get("maxArrivalTime")

            query = """
                        SELECT f.flight_id, f.departure_airport_id, f.arrival_airport_id, f.departure_time, f.travel_time, f.price
                        FROM flights f
                        JOIN airports dep_airport ON f.departure_airport_id = dep_airport.id
                        JOIN airports arr_airport ON f.arrival_airport_id = arr_airport.id
                        WHERE 1=1
                    """
            query_params = []

            if departure_city:
                city = CityService.get_city_by_name(departure_city)
                if city is not None:
                    dep_city_id = city.get("city_id")
                    query += " AND dep_airport.city_id = %s"
                    query_params.append(dep_city_id)

            if arrival_city:
                city = CityService.get_city_by_name(arrival_city)
                if city is not None:
                    arrival_city_id = city.get("city_id")
                    query += " AND arr_airport.city_id = %s"
                    query_params.append(arrival_city_id)

            if min_price is not None:
                query += " AND f.price >= %s"
                query_params.append(min_price)

            if max_price is not None:
                query += " AND f.price <= %s"
                query_params.append(max_price)

            if min_departure_time:
                min_departure_time_obj = datetime.strptime(min_departure_time, "%H:%M").time()
                query += " AND f.departure_time >= %s"
                query_params.append(min_departure_time_obj)

            if max_departure_time:
                max_departure_time_obj = datetime.strptime(max_departure_time, "%H:%M").time()
                query += " AND f.departure_time <= %s"
                query_params.append(max_departure_time_obj)

            if max_travel_time is not None:
                query += " AND f.travel_time <= %s"
                query_params.append(max_travel_time)

            if min_arrival_time:
                min_arrival_time_obj = datetime.strptime(min_arrival_time, "%H:%M").time()
                query += " AND (f.departure_time + interval '1 minute' * f.travel_time) >= %s"
                query_params.append(min_arrival_time_obj)

            if max_arrival_time:
                max_arrival_time_obj = datetime.strptime(max_arrival_time, "%H:%M").time()
                query += " AND (f.departure_time + interval '1 minute' * f.travel_time) <= %s"
                query_params.append(max_arrival_time_obj)

            with connection.cursor() as cursor:
                cursor.execute(query, tuple(query_params))
                flights = cursor.fetchall()

            flight_list = [
                {
                    "id": flight[0],
                    "departure_airport_id": flight[1],
                    "arrival_airport_id": flight[2],
                    "departure_time": flight[3].strftime('%H:%M') if flight[3] else None,
                    "travel_time": flight[4],
                    "price": flight[5]
                }
                for flight in flights
            ]

            return {"flights": flight_list}

        except Exception as e:
            return {"error": f"Error searching flights: {str(e)}"}

        finally:
            if 'connection' in locals():
                connection.close()

    @classmethod
    def get_flight(cls, flight_id):
        connection = get_connection()

        if connection is None:
            return {"error": "Could not establish a database connection"}

        try:
            query = """
                    SELECT flight_id, departure_airport_id, arrival_airport_id, departure_time, travel_time, price
                    FROM flights
                    WHERE flight_id = %s
                """

            with connection.cursor() as cursor:
                cursor.execute(query, (flight_id,))
                flight = cursor.fetchone()

                if flight is None:
                    return {"error": f"Flight with ID {flight_id} not found"}

                flight_data = {
                    "id": flight[0],
                    "departure_airport_id": flight[1],
                    "arrival_airport_id": flight[2],
                    "departure_time": flight[3].strftime('%H:%M') if flight[3] else None,
                    "travel_time": flight[4],
                    "price": flight[5]
                }

                return {"flight": flight_data}

        except Exception as e:
            return {"error": f"Error fetching flight: {str(e)}"}

        finally:
            if 'connection' in locals():
                connection.close()

    @classmethod
    def update_flight(cls, flight_id, json):
        connection = get_connection()

        if connection is None:
            return {"error": "Could not establish a database connection"}

        try:
            departure_airport_id = json.get("departureAirport")
            arrival_airport_id = json.get("arrivalAirport")
            departure_time = json.get("departureTime")
            travel_time = json.get("travelTime")
            price_str = json.get("price")

            price = None
            if price_str is not None:
                try:
                    price = float(price_str.replace('$', ''))
                except ValueError:
                    return {
                        "error": f"Invalid price format: {price_str}. Ensure it's a valid number with or without a dollar sign."}

            if not any([departure_airport_id, arrival_airport_id, departure_time, travel_time, price]):
                return {"error": "No fields provided to update"}

            update_fields = []
            query_params = []

            if departure_airport_id is not None:
                update_fields.append("departure_airport_id = %s")
                query_params.append(departure_airport_id)

            if arrival_airport_id is not None:
                update_fields.append("arrival_airport_id = %s")
                query_params.append(arrival_airport_id)

            if departure_time is not None:
                try:
                    departure_time_obj = datetime.strptime(departure_time, "%H:%M")
                    update_fields.append("departure_time = %s")
                    query_params.append(departure_time_obj)
                except ValueError:
                    return {"error": f"Invalid departure time format: {departure_time}. Use 'HH:MM' format."}

            if travel_time is not None:
                update_fields.append("travel_time = %s")
                query_params.append(travel_time)

            if price is not None:
                update_fields.append("price = %s")
                query_params.append(price)

            query_params.append(flight_id)
            update_query = f"UPDATE flights SET {', '.join(update_fields)} WHERE flight_id = %s"

            with connection.cursor() as cursor:
                cursor.execute(update_query, tuple(query_params))
                rows_updated = cursor.rowcount
                connection.commit()

                if rows_updated > 0:
                    return {"message": f"Flight with ID {flight_id} has been updated successfully"}
                else:
                    return {"error": "Flight not found or no changes were made"}

        except Exception as e:
            connection.rollback()
            return {"error": f"Error updating flight: {str(e)}"}

        finally:
            if 'connection' in locals():
                connection.close()

    @classmethod
    def delete_flight(cls, flight_id):
        connection = get_connection()

        if connection is None:
            return {"error": "Could not establish a database connection"}

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT flight_id FROM flights WHERE flight_id = %s", (flight_id,))
                flight = cursor.fetchone()

                if flight is None:
                    return {"error": "Flight not found"}

                cursor.execute("DELETE FROM flights WHERE flight_id = %s", (flight_id,))
                rows_deleted = cursor.rowcount
                connection.commit()

                if rows_deleted > 0:
                    return {"message": f"Flight with ID {flight_id} has been deleted successfully"}
                else:
                    return {"error": "Failed to delete the flight"}

        except Exception as e:
            if 'connection' in locals():
                connection.rollback()
            return {"error": f"Error deleting flight: {str(e)}"}

        finally:
            if 'connection' in locals():
                connection.close()
