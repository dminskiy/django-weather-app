from django.db import models
from django.utils import timezone


class City(models.Model):
    id = models.AutoField(primary_key=True)
    lon = models.FloatField(null=False, editable=False)
    lat = models.FloatField(null=False, editable=False)
    city_name = models.TextField(null=False, editable=False)
    country_code = models.TextField(null=True, editable=False)

    created_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        name_country = (
            f"{self.city_name}"
            if not self.country_code
            else f"{self.city_name}, {self.country_code}"
        )
        return f"{name_country} [lon: {self.lon}; lat: {self.lat}]"

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "City"
        unique_together = (("lon", "lat"),)


class CityWeather(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.OneToOneField(
        "City",
        models.DO_NOTHING,
    )
    current_temperature_K = models.FloatField(null=True, blank=True, editable=True)
    current_temperature_C = models.FloatField(null=True, blank=True, editable=True)
    current_condition = models.TextField(null=True, blank=True, editable=True)
    humidity = models.IntegerField(null=True, blank=True, editable=True)
    wind_speed = models.FloatField(null=True, blank=True, editable=True)

    weather_raw = models.JSONField(null=True, blank=True, editable=True)
    created_at = models.DateTimeField(null=True)
    last_updated = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.last_updated = timezone.now()
        if self.current_temperature_K:
            self.current_temperature_C = self._kelvin_to_celcius()

        super().save(*args, **kwargs)

    def _kelvin_to_celcius(self):
        if not self.current_temperature_K:
            return None
        else:
            return round(self.current_temperature_K - 273.15, 1)

    class Meta:
        managed = True
        db_table = "CityWeather"
