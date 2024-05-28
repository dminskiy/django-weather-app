from rest_framework import serializers
from city_weather.models import City, CityWeather


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        return value.strftime("%d %b %Y %H:%M:%S")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        exclude = ["created_at"]


class CityWeatherSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    last_updated = CustomDateTimeField()

    class Meta:
        model = CityWeather
        exclude = ["created_at", "current_temperature_K", "weather_raw"]
