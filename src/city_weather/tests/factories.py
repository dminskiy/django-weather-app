import factory
from city_weather import models
from faker import Faker
from factory import SubFactory

fake = Faker()


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.City

    lon = -84.2529869
    lat = 38.2097987
    city_name = "Paris"
    country_code = "FR"


class CityWeatherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CityWeather

    city = SubFactory(CityFactory)
    current_temperature_K = fake.pyfloat()
    current_condition = fake.text()
    humidity = fake.pyint()
    wind_speed = fake.pyfloat()
    weather_raw = fake.json()
