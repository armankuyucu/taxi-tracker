from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from mongoengine import connect, disconnect
from datetime import datetime
from taxi_tracker.models import TaxiLocations, Car


class IntegrationTest(TestCase):
    """ This class tests the integration of the user registration, login, and map view access. """
    
    def setUp(self):
        # Disconnect from any existing connection with the alias 'core', then connect to the test database
        disconnect(alias='core')
        connect('taxi_tracker_test', alias='core')

        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.map_view_url = reverse('map_view')

        self.user_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        self.car_data = {
            'cars': ['1', '2']
        }

        # Create taxi locations for testing in the database
        for car_id in self.car_data['cars']:
            TaxiLocations.objects.create(date_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                         latitude="0.0", longitude="0.0", car_id=car_id)

    def tearDown(self):
        # Clean up the database
        TaxiLocations.objects.filter(car_id__in=self.car_data['cars']).delete()
        disconnect(alias='core')

    def test_user_registration_login_and_map_view_access(self):
        # Register the user
        response = self.client.post(self.register_url, {**self.user_data, **self.car_data})
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(login_response.status_code, 302)  # Redirect after login
        self.assertRedirects(login_response, self.map_view_url)
        
        # Access the map view
        map_view_response = self.client.get(self.map_view_url)
        self.assertEqual(map_view_response.status_code, 200)
        self.assertTemplateUsed(map_view_response, 'base/map_view.html')

        # Check if the cars are assigned to the user
        user = User.objects.get(username='testuser')
        self.assertTrue(Car.objects.filter(user=user, car_id='1').exists())
        self.assertTrue(Car.objects.filter(user=user, car_id='2').exists())
