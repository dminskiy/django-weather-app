# Generated by Django 5.0.6 on 2024-05-28 16:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("lon", models.FloatField(editable=False)),
                ("lat", models.FloatField(editable=False)),
                ("city_name", models.TextField(editable=False)),
                ("country_code", models.TextField(editable=False, null=True)),
                ("created_at", models.DateTimeField(null=True)),
            ],
            options={
                "db_table": "City",
                "managed": True,
                "unique_together": {("lon", "lat")},
            },
        ),
        migrations.CreateModel(
            name="CityWeather",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("current_temperature_K", models.FloatField(blank=True, null=True)),
                ("current_temperature_C", models.FloatField(blank=True, null=True)),
                ("current_condition", models.TextField(blank=True, null=True)),
                ("humidity", models.IntegerField(blank=True, null=True)),
                ("wind_speed", models.FloatField(blank=True, null=True)),
                ("weather_raw", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(null=True)),
                ("last_updated", models.DateTimeField(null=True)),
                (
                    "city",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="city_weather.city",
                    ),
                ),
            ],
            options={
                "db_table": "CityWeather",
                "managed": True,
            },
        ),
    ]
