# taxi_tracker/apps.py
from django.apps import AppConfig


class TaxiTrackerConfig(AppConfig):
    name = 'taxi_tracker'

    def ready(self):
        from . import data_service
        data_service.populate_database()
