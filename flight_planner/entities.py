from datetime import datetime


class Flight:

    def __init__(self, departure_airport_id, arrival_airport_id, departure_time, travel_time, price, flight_id=None):

        self.flight_id = flight_id
        self.departure_airport_id = departure_airport_id
        self.arrival_airport_id = arrival_airport_id
        self.departure_time = datetime.strptime(departure_time, '   %H:%M')
        self.travel_time = travel_time
        self.price = price

    def to_dict(self):

        return {
            "flight_id": self.flight_id,
            "departureAirport": self.departure_airport_id,
            "arrivalAirport": self.arrival_airport_id,
            "departureTime": self.departure_time.strftime('%H:%M'),
            "travelTime": self.travel_time,
            "price": self.price
        }
