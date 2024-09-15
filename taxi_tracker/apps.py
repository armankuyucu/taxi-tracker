# taxi_tracker/apps.py
from django.apps import AppConfig
import logging

class TaxiTrackerConfig(AppConfig):
    name = 'taxi_tracker'

    def ready(self):
        logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO
        from . import data_service
        data_service.populate_database('taxi_tracker')
