import csv

import mongoengine

import logging
from taxi_tracker.models import TaxiLocations


def save_taxi_locations(date_time: str, latitude: float, longitude: float, car_id: int):
    """
    Save TaxiLocations to the MongoDB database.
    :param date_time: The datetime string.
    :param latitude: The latitude coordinate.
    :param longitude: The longitude coordinate.
    :param car_id: The unique identifier of the car.
    """
    try:
        # Use keyword arguments for clarity and type checking
        taxi_data = TaxiLocations(
            date_time=date_time,
            latitude=latitude,
            longitude=longitude,
            car_id=car_id
        )
        taxi_data.save()  # Save the document to the database
    except mongoengine.ValidationError as e:
        logging.error(f"Validation error happened while creating car: {e}")


def populate_database():
    """ Read the taxi locations from the csv file and create data in MongoDB, but only if not already created """
    try:
        mongoengine.register_connection(alias='core', name='taxi-tracker')

        # Check if the collection is empty
        if TaxiLocations.objects.count() > 0:
            logging.info("Data already exists in the database. Skipping CSV import.")
            return  # Exit the function if data already exists

        with open('static/cars.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                save_taxi_locations(line[0], float(line[1]), float(line[2]), int(line[3]))

        logging.info("Data imported successfully from CSV.")
    except Exception as e:
        logging.error(f"An error occurred, couldn't populate MongoDB: {e}")
