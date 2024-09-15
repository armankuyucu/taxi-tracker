import mongoengine
from django.db import models
from django.contrib.auth.models import User


class TaxiLocations(mongoengine.Document):
    date_time = mongoengine.StringField(required=True)
    latitude = mongoengine.FloatField(required=True)
    longitude = mongoengine.FloatField(required=True)
    car_id = mongoengine.IntField(required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'taxiLocations'
    }


class Car(models.Model):
    # cascade means when a user is deleted their cars will be deleted too
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    car_id = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.user.username}'s Car: {self.car_id}"
