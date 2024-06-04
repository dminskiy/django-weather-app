import json

from rest_framework.views import APIView
from django.http import JsonResponse

from dataclasses import asdict
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from city_weather.models import City, CityWeather
from city_weather.services.open_weather_api import OpenWeatherAPI
from city_weather.serializers import CityWeatherSerializer

openWeatherApi = OpenWeatherAPI()


def autocomplete(request):
    query = request.GET.get("q", "")
    if query:
        cities = openWeatherApi.get_cities(city_name=query, limit=10)
        cities_dict = [asdict(item) for item in cities]
        return JsonResponse(cities_dict, safe=False)
    return JsonResponse([], safe=False)


class CityWeatherView(APIView):
    def get(self, request):
        """
        Get all cities and render the index page
        """
        cities = CityWeather.objects.all()
        serializer = CityWeatherSerializer(cities, many=True)

        return render(request, "main/index.html", {"cities": serializer.data})

    def post(self, request):
        """
        Get weather: adds a city or updates one if it already exists
        """
        request_dict = request.data
        city_data = request_dict.get("city_raw")

        if city_data:
            if not isinstance(city_data, dict):
                city_data = json.loads(city_data)

            lon = city_data["lon"]
            lat = city_data["lat"]
            weather_info = openWeatherApi.get_weather(lat=lat, lon=lon)

            city = City.objects.get_or_create(
                city_name=city_data["city_name"],
                lon=lon,
                lat=lat,
                country_code=city_data.get("country_code"),
                state=city_data.get("state"),
            )[0]
            city_weather = CityWeather.objects.get_or_create(city=city)[0]

            city_weather.current_temperature_K = weather_info.current_temperature_kelvin
            city_weather.current_condition = weather_info.current_condition
            city_weather.humidity = weather_info.humidity
            city_weather.wind_speed = weather_info.wind_speed
            city_weather.weather_raw = weather_info.weather_raw
            city_weather.save()

            cities = CityWeather.objects.all()
            serializer = CityWeatherSerializer(cities, many=True)

            return JsonResponse({"cities": serializer.data})
        return JsonResponse({"error": "Invalid POST request"}, status=400)

    def delete(self, request):
        """
        Delete a city from the database
        """
        request_dict = request.data
        city_id = request_dict.get("id")
        if city_id:
            city = get_object_or_404(City, id=city_id)
            city_weather = get_object_or_404(CityWeather, city__id=city.id)
            city_weather.delete()
            city.delete()
            return JsonResponse({"success": True})
        return JsonResponse({"error": "Invalid DELETE request"}, status=400)
