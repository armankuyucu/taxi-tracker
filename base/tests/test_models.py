from mongoengine import connect, disconnect
from django.test import TestCase
from django.contrib.auth.models import User
from taxi_tracker.models import TaxiLocations, Car


class TaxiLocationsTestCase(TestCase):

    def setUp(self):
        # Disconnect from any existing connection with the alias 'core', then connect to the test database
        disconnect(alias='core')
        connect('mongoenginetest', alias='core')
        self.taxi_location = TaxiLocations(
            date_time="2023-10-01 12:00:00",
            latitude=40.7128,
            longitude=-74.0060,
            car_id=1
        )

    def tearDown(self):
        self.taxi_location.delete()
        # Disconnect from the test database
        disconnect(alias='core')

    def test_create_taxi_location(self):
        self.taxi_location.save()

        # Retrieve the saved taxi location
        saved_location = TaxiLocations.objects.get(car_id=1)
        self.assertEqual(saved_location.date_time, "2023-10-01 12:00:00")
        self.assertEqual(saved_location.latitude, 40.7128)
        self.assertEqual(saved_location.longitude, -74.0060)
        self.assertEqual(saved_location.car_id, 1)

    def test_update_taxi_location(self):
        self.taxi_location.save()

        # Update the taxi location
        self.taxi_location.update(set__latitude=41.0)
        updated_location = TaxiLocations.objects.get(car_id=1)
        self.assertEqual(updated_location.latitude, 41.0)

    def test_delete_taxi_location(self):
        taxi_location = TaxiLocations(
            date_time="2023-10-01 12:00:00",
            latitude=40.7128,
            longitude=-74.0060,
            car_id=1
        )
        taxi_location.save()

        # Delete the taxi location
        taxi_location.delete()
        with self.assertRaises(TaxiLocations.DoesNotExist):
            TaxiLocations.objects.get(car_id=1)


class CarTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_car(self):
        car = Car.objects.create(user=self.user, car_id=1)
        self.assertEqual(car.user.username, 'testuser')
        self.assertEqual(car.car_id, 1)

    def test_update_car(self):
        car = Car.objects.create(user=self.user, car_id=1)
        car.car_id = 2
        car.save()

        updated_car = Car.objects.get(id=car.id)
        self.assertEqual(updated_car.car_id, 2)

    def test_delete_car(self):
        car = Car.objects.create(user=self.user, car_id=1)
        car_id = car.id
        car.delete()

        with self.assertRaises(Car.DoesNotExist):
            Car.objects.get(id=car_id)

    def test_cascade_delete_user(self):
        # Delete the user and check if the car is deleted as well
        Car.objects.create(user=self.user, car_id=1)
        self.user.delete()

        with self.assertRaises(Car.DoesNotExist):
            Car.objects.get(car_id=1)
