from flight_planner.connection_pg import get_connection
from flight_planner.entities import Flight


class CityStorage:
    def create(self, name):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO cities (city_name) VALUES (%s)", (name,))

                cursor.execute("SELECT city_name, id FROM cities WHERE city_name = %s", (name,))
                new_city_id = cursor.fetchone()[1]

            connection.commit()

            return {"id": new_city_id, "name": name}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            connection.close()

    def get_all(self):
        connection = get_connection()

        if connection is None:
            return {"error": "Could not establish a database connection"}

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT city_name FROM cities")
                cities = cursor.fetchall()

            city_list = [{"city_name": city[0]} for city in cities]

            return {"cities": city_list}

        except Exception as e:
            return {"error": str(e)}

        finally:
            connection.close()

    def get(self, city_id):
        connection = get_connection()

        if connection is None:
            raise KeyError("Could not establish a database connection")

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT city_name FROM cities WHERE id = %s", (city_id,))
                city = cursor.fetchone()

            if city is None:
                return None

            return {"city_id": city_id, "city_name": city[0]}


        except KeyError as e:
            return {"error": str(e)}

        except Exception as e:
            return {"error": str(e)}

        finally:
            connection.close()

    def get_by_name(self, name):
        connection = get_connection()

        if connection is None:
            return {"error": "Could not establish a database connection"}

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT city_name, id FROM cities WHERE city_name = %s", (name,))
                city = cursor.fetchone()

            if city is None:
                return None

            return {"city_id": city[1], "city_name": name}

        except Exception as e:
            return {"error": str(e)}

        finally:
            connection.close()

    def delete(self, city_id):
        connection = get_connection()

        if connection is None:
            return {"error": "Could not establish a database connection"}

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT city_name FROM cities WHERE id = %s", (city_id,))
                city = cursor.fetchone()

            if city is None:
                return {"error": "City not found"}

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM cities WHERE id = %s", (city_id,))

            connection.commit()

            return {"message": f"City with ID {city_id} deleted successfully"}

        except Exception as e:
            return {"error": str(e)}

        finally:
            connection.close()

    def delete_all(self):
        connection = get_connection()

        if connection is None:
            return {"error": "Could not establish a database connection"}

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM cities")

            connection.commit()

            return {"message": "All cities have been deleted successfully"}

        except Exception as e:
            return {"error": str(e)}

        finally:
            connection.close()


class AirportStorage:
    def create(self, name, city):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO airports (city_id, name) VALUES (%s, %s)",
                    (city, name)
                )

            connection.commit()

            return {"message": "Airport created successfully"}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            connection.close()

    def get_all(self):
        connection = get_connection()

        if connection is None:
            return {"error": "Could not establish a database connection"}

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, city_id FROM airports")
                airports = cursor.fetchall()

                airport_list = []
                for airport in airports:
                    airport_dict = {
                        "id": airport[0],
                        "name": airport[1],
                        "city_id": airport[2]
                    }
                    airport_list.append(airport_dict)

                return {"airports": airport_list}

        except Exception as e:
            return {"error": f"Error fetching airports: {str(e)}"}

        finally:
            connection.close()

    def get(self, airport_id):
        connection = get_connection()

        if connection is None:
            return {"error": "Could not establish a database connection"}

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, city_id FROM airports WHERE id = %s", (airport_id,))

                airport = cursor.fetchone()

                if airport is None:
                    return {"error": "Airport not found"}

                airport_dict = {
                    "id": airport[0],
                    "name": airport[1],
                    "city_id": airport[2]
                }

                return {"airport": airport_dict}

        except Exception as e:
            return {"error": f"Error fetching airport: {str(e)}"}

        finally:
            connection.close()

    def delete(self, airport_id):
        connection = get_connection()

        if connection is None:
            return {"error": "Could not establish a database connection"}

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM airports WHERE id = %s", (airport_id,))

                rows_deleted = cursor.rowcount

                connection.commit()

                if rows_deleted > 0:
                    return {"message": f"Airport with ID {airport_id} has been deleted successfully"}
                else:
                    return {"error": "Airport not found"}

        except Exception as e:
            connection.rollback()
            return {"error": f"Error deleting airport: {str(e)}"}

        finally:
            connection.close()

    def delete_all(self):
        connection = get_connection()

        if connection is None:
            return {"error": "Could not establish a database connection"}

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM airports")

            connection.commit()

            return {"message": "All airports have been deleted successfully"}

        except Exception as e:
            return {"error": f"Error deleting airports: {str(e)}"}

        finally:
            connection.close()


class FlightStorage:
    def create(self, departure_airport_id, arrival_airport_id, departure_time, travel_time, price):
        try:

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

        except Exception as e:
            if 'connection' in locals():
                connection.rollback()
            return {"error": f"Error creating flight: {str(e)}"}
        finally:
            if 'connection' in locals():
                connection.close()

        return flight

    def delete(self, flight_id):
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

    def delete_all(self):
        connection = get_connection()

        if connection is None:
            return {"error": "Could not establish a database connection"}

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM flights")
                rows_deleted = cursor.rowcount
                connection.commit()

                if rows_deleted > 0:
                    return {"message": f"All {rows_deleted} flights have been deleted successfully"}
                else:
                    return {"message": "No flights to delete"}

        except Exception as e:
            if 'connection' in locals():
                connection.rollback()
            return {"error": f"Error deleting flights: {str(e)}"}

        finally:
            if 'connection' in locals():
                connection.close()

    def get(self, flight_id):
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

    def get_all(self):
        def get_all(self):
            connection = get_connection()

            if connection is None:
                return {"error": "Could not establish a database connection"}

            try:
                query = """
                              SELECT flight_id, departure_airport_id, arrival_airport_id, departure_time, travel_time, price
                              FROM flights
                          """

                with connection.cursor() as cursor:
                    cursor.execute(query)
                    flights = cursor.fetchall()

                    if not flights:
                        return {"error": "No flights found"}

                    flights_data = []
                    for flight in flights:
                        flight_data = {
                            "id": flight[0],
                            "departure_airport_id": flight[1],
                            "arrival_airport_id": flight[2],
                            "departure_time": flight[3].strftime('%H:%M') if flight[3] else None,
                            "travel_time": flight[4],
                            "price": flight[5]
                        }
                        flights_data.append(flight_data)

                    return {"flights": flights_data}

            except Exception as e:
                return {"error": f"Error fetching flights: {str(e)}"}

            finally:
                if 'connection' in locals():
                    connection.close()
