from typing import Optional, List
from dataclasses import dataclass

import os
import requests
import json


@dataclass
class CityInfo:
    city_name: str
    lon: float
    lat: float
    city_raw: Optional[dict]
    country_code: Optional[str] = None
    state: Optional[str] = None
    label: Optional[str] = None

    def __post_init__(self):
        self.label = f"{self.city_name}"
        if self.state:
            self.label += f", {self.state}"
        if self.country_code:
            self.label += f", {self.country_code}"


@dataclass
class WeatherInfo:
    current_temperature_kelvin: float
    current_condition: str
    humidity: int
    wind_speed: float
    weather_raw: dict


class OpenWeatherAPI:
    def __init__(self) -> None:
        self.appid = os.environ.get("OPEN_WEATHER_API_KEY")
        assert self.appid, "OpenWeather API key was not provided"

    def get_weather(self, lat: float, lon: float) -> WeatherInfo:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.appid}"

        response = requests.get(url)

        if response.status_code != 200:
            raise ConnectionError(
                f"Could not get weather info. Unexpected response status: {response.status_code}"
            )

        data = json.loads(response.content)

        return WeatherInfo(
            current_temperature_kelvin=data["main"]["temp"],
            current_condition=data["weather"][0]["main"],
            humidity=data["main"]["humidity"],
            wind_speed=data["wind"]["speed"],
            weather_raw=data,
        )

    def get_cities(
        self, city_name: str, country_code: Optional[str] = None, limit: int = 1
    ) -> List[CityInfo]:
        name_country = (
            f"{city_name}" if not country_code else f"{city_name},{country_code}"
        )

        url = f"http://api.openweathermap.org/geo/1.0/direct?q={name_country}&limit={limit}&appid={self.appid}"

        response = requests.get(url)

        if response.status_code != 200:
            raise ConnectionError(
                f"Could not get city info. Unexpected response status: {response.status_code}"
            )

        data = json.loads(response.content)

        return [
            CityInfo(
                city_name=item["name"],
                lon=item["lon"],
                lat=item["lat"],
                country_code=item["country"],
                state=item.get("state", None),
                city_raw=item,
            )
            for item in data
        ]
