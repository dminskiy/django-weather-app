from django.db import models
from django.utils import timezone


class City(models.Model):
    id = models.AutoField(primary_key=True)
    lon = models.FloatField(null=False, editable=False)
    lat = models.FloatField(null=False, editable=False)
    city_name = models.TextField(null=False, editable=False)
    country_code = models.TextField(null=True, editable=False)

    city_raw = models.JSONField(editable=False)
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
    city = models.ForeignKey(
        "City",
        models.DO_NOTHING,
        null=False,
        blank=False,
        editable=False,
    )
    current_temperature_K = models.FloatField(null=False, editable=True)
    current_condition = models.TextField(null=False, editable=True)

    weather_raw = models.JSONField(editable=True)
    created_at = models.DateTimeField(null=True)
    last_updated = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        if not self.last_updated:
            self.last_updated = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "CityWeather"
