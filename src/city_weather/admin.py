from django.contrib import admin
from city_weather.models import City, CityWeather


class CityAdmin(admin.ModelAdmin):
    list_display = (
        "city_name",
        "country_code",
        "lon",
        "lat",
        "created_at",
    )
    list_filter = (
        "city_name",
        "country_code",
        "created_at",
    )


class CityWeatherAdmin(admin.ModelAdmin):
    list_display = (
        "city",
        "current_temperature_K",
        "current_condition",
        "created_at",
        "last_updated",
    )
    list_filter = (
        "city__city_name",
        "city__country_code",
        "created_at",
        "last_updated",
        "current_condition",
    )


admin.site.register(City, CityAdmin)
admin.site.register(CityWeather, CityWeatherAdmin)
