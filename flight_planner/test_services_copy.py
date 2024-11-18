import unittest
from unittest.mock import patch, MagicMock
from flight_planner.services import CityService, AirportService, FlightService

# FILE: flight_planner/test_services.py


class TestCityService(unittest.TestCase):

    @patch('flight_planner.services.CityStorage')
    def test_create_city(self, mock_city_storage):
        mock_storage_instance = mock_city_storage.return_value
        mock_storage_instance.create.return_value = {'id': 1, 'name': 'Test City'}

        response = CityService.create_city({'name': 'Test City'})
        self.assertEqual(response, {'id': 1, 'name': 'Test City'})

    @patch('flight_planner.services.CityStorage')
    def test_get_all_cities(self, mock_city_storage):
        mock_storage_instance = mock_city_storage.return_value
        mock_storage_instance.get_all.return_value = [{'id': 1, 'name': 'Test City'}]

        response = CityService.get_all_cities()
        self.assertEqual(response, [{'id': 1, 'name': 'Test City'}])

    @patch('flight_planner.services.CityStorage')
    def test_get_city(self, mock_city_storage):
        mock_storage_instance = mock_city_storage.return_value
        mock_storage_instance.get.return_value = {'id': 1, 'name': 'Test City'}

        response = CityService.get_city(1)
        self.assertEqual(response, {'id': 1, 'name': 'Test City'})

    @patch('flight_planner.services.CityStorage')
    def test_get_city_by_name(self, mock_city_storage):
        mock_storage_instance = mock_city_storage.return_value
        mock_storage_instance.get_by_name.return_value = {'id': 1, 'name': 'Test City'}

        response = CityService.get_city_by_name('Test City')
        self.assertEqual(response, {'id': 1, 'name': 'Test City'})

    @patch('flight_planner.services.CityStorage')
    def test_get_city_not_found(self, mock_city_storage):
        mock_storage_instance = mock_city_storage.return_value
        mock_storage_instance.get.return_value = None

        with self.assertRaises(KeyError) as context:
            CityService.get_city(1)

    @patch('flight_planner.services.CityStorage')
    def test_delete_city(self, mock_city_storage):
        response = CityService.delete_city(1)
        self.assertEqual(response, '')

    @patch('flight_planner.services.CityStorage')
    def test_delete_all_cities(self, mock_city_storage):
        response = CityService.delete_all_cities()
        self.assertEqual(response, '')

class TestAirportService(unittest.TestCase):

    @patch('flight_planner.services.CityStorage')
    @patch('flight_planner.services.AirportStorage')
    def test_create_airport(self, mock_airport_storage, mock_city_service):
        mock_storage_instance = mock_airport_storage.return_value
        mock_city_instance = mock_city_service.return_value

        mock_storage_instance.create.return_value = {'id': 1, 'name': 'Test Airport','city': 1}
        mock_city_instance.get_city.return_value = {'id': 1, 'name': 'Test City'}

        response = AirportService.create_airport({'name': 'Test Airport', 'city': 1})
        self.assertEqual(response, {'id': 1, 'name': 'Test Airport', 'city': 1})

    @patch('flight_planner.services.AirportStorage')
    def test_get_all_airports(self, mock_city_storage):
        mock_storage_instance = mock_city_storage.return_value
        mock_storage_instance.get_all.return_value = [{'id': 1, 'name': 'Test Airport','city': 1}]

        response = AirportService.get_all_airports()
        self.assertEqual(response, [{'id': 1, 'name': 'Test Airport', 'city': 1}])

    @patch('flight_planner.services.AirportStorage')
    def test_get_airport(self, mock_city_storage):
        mock_storage_instance = mock_city_storage.return_value
        mock_storage_instance.get_airport.return_value = {'id': 1, 'name': 'Test Airport', 'city': 1}

        response = AirportService.get_airport(1)
        self.assertEqual(response, {'id': 1, 'name': 'Test Airport', 'city': 1})

    @patch('flight_planner.services.AirportStorage')
    def test_get_airport_not_found(self, mock_city_storage):
        mock_storage_instance = mock_city_storage.return_value
        mock_storage_instance.get.return_value = None

        with self.assertRaises(KeyError) as context:
            AirportService.get_airport(1)

    @patch('flight_planner.services.AirportStorage')
    def test_delete_airport(self, mock_city_storage):
        response = AirportService.delete_airport(1)
        self.assertEqual(response, '')

    @patch('flight_planner.services.AirportStorage')
    def test_delete_all_airports(self, mock_city_storage):
        response = AirportService.delete_all_airports()
        self.assertEqual(response, '')

class TestFlightService(unittest.TestCase):

    
    def test_create_flight(self):
        mock_storage.create_flight.return_value = {'id': 1, 'name': 'Test Flight'}
        response = FlightService.create_flight({'name': 'Test Flight'})
        self.assertEqual(response, {'id': 1, 'name': 'Test Flight'})

    
    def test_get_all_flights(self):
        mock_storage.get_all_flights.return_value = [{'id': 1, 'name': 'Test Flight'}]
        response = FlightService.get_all_flights()
        self.assertEqual(response, [{'id': 1, 'name': 'Test Flight'}])

    
    def test_get_flight(self):
        mock_storage.get_flight.return_value = {'id': 1, 'name': 'Test Flight'}
        response = FlightService.get_flight(1)
        self.assertEqual(response, {'id': 1, 'name': 'Test Flight'})

    
    def test_get_flight_not_found(self):
        mock_storage.get_flight.return_value = None
        with self.assertRaises(KeyError) as context:
            FlightService.get_flight(1)

    
    def test_delete_flight(self):
        response = FlightService.delete_flight(1)
        self.assertEqual(response, '')

    
    def test_delete_all_flights(self):
        response = FlightService.delete_all_flights()
        self.assertEqual(response, '')

if __name__ == '__main__':
    unittest.main()