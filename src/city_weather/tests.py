from rest_framework.test import APITestCase
from city_weather.services.open_weather_api import OpenWeatherAPI


class OpenWeatherAPITest(APITestCase):
    def test_get_cities_norm(self):
        # Testing variables
        city = "London"
        country = "GB"
        ow = OpenWeatherAPI()

        city_info = ow.get_cities(city, country)

        self.assertEqual(len(city_info), 1)
        self.assertEqual(city_info[0].city_name, city)
        self.assertEqual(city_info[0].country_code, country)

    def test_get_cities_non_existent(self):
        # Testing variables
        city = "London"
        country = "UK"
        ow = OpenWeatherAPI()

        city_info = ow.get_cities(city, country)

        self.assertEqual(len(city_info), 0)

    def test_get_weather_info_norm(self):
        # Testing variables
        city = "London"
        country = "GB"
        ow = OpenWeatherAPI()

        city_info = ow.get_cities(city, country, 1)[0]
        weather_info = ow.get_weather(city_info=city_info)

        self.assertGreater(weather_info.current_temperature_kelvin, 0)
        self.assertEqual(weather_info.weather_raw["name"], city)
