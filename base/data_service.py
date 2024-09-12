import mongoengine

from base.cars import Cars


def create_cars(date_time: str, latitude: float, longitude: float, car_id: int, user_id: int):
    cars = Cars()
    cars.date_time = date_time
    cars.latitude = latitude
    cars.longitude = longitude
    cars.car_id = car_id
    cars.user_id = user_id
    cars.save()
