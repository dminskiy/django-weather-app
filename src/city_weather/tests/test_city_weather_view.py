from django.test import TestCase
from city_weather.tests.factories import CityWeatherFactory
from city_weather.models import City, CityWeather
from django.urls import reverse
import json


class TestCityWeatherView(TestCase):
    def setUp(self):
        self.city_weather = CityWeatherFactory()

    def test_create_city(self):
        all_cities = City.objects.all()
        all_city_weather = CityWeather.objects.all()

        self.assertEqual(all_cities.count(), 1)
        self.assertEqual(all_cities.count(), all_city_weather.count())
        self.assertEqual(all_cities[0].city_name, self.city_weather.city.city_name)

    def test_autocomplete(self):
        response = self.client.post(
            reverse("autocomplete"),
            data=json.dumps({"q": "London"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

    def test_get_view(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.city_weather.city.city_name)

    def test_index_template(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "main/index.html")

    def test_post_view(self):
        response = self.client.post(
            reverse("get_weather_and_update"),
            data=json.dumps(
                {
                    "city_raw": {
                        "city_name": "Paris",
                        "lat": 48.8458,
                        "lon": 2.3509,
                    }
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_view(self):
        response = self.client.delete(
            reverse("delete_city"),
            data=json.dumps({"id": 1}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(City.objects.all().count(), 0)
