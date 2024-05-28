from pytest_factoryboy import register

from city_weather.tests.factories import (
    CityFactory,
    CityWeatherFactory,
)

register(CityFactory)
register(CityWeatherFactory)
