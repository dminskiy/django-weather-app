from django.urls import path
from city_weather.views import CityWeatherView, autocomplete

urlpatterns = [
    path("", CityWeatherView.as_view(), name="index"),
    path("autocomplete/", autocomplete, name="autocomplete"),
    path(
        "get_weather_and_update/",
        CityWeatherView.as_view(),
        name="get_weather_and_update",
    ),
    path("delete_city/", CityWeatherView.as_view(), name="delete_city"),
]
