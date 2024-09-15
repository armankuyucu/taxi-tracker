from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
from mongoengine import connect, disconnect
from taxi_tracker.models import TaxiLocations, Car


class TestViews(TestCase):

    def setUp(self):
        # Disconnect from any existing connection with the alias 'core', then connect to the test database
        disconnect(alias='core')
        connect('taxi_tracker_test', alias='core')

        self.client = Client()
        self.map_view_url = reverse('map_view')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.register_url = reverse('register')

        self.user_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        self.car_data = {
            'cars': ['1', '2']
        }

    def test_map_view_get(self):
        # Create a test user and login, because map_view is restricted to authenticated users
        User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(self.map_view_url)

        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'base/map_view.html')

    def test_login_get(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_success(self):
        User.objects.create_user(username='testuser', password='testpassword')

        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })

        self.assertEqual(response.status_code, 302) # Redirect after login
        self.assertRedirects(response, self.map_view_url)

    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'invalidpassword'
        })

        self.assertEqual(response.status_code, 200)
        # Check if the form has the correct error message
        self.assertIn(('Please enter a correct username and password. Note that both fields may be case-sensitive.'),
                      response.context['form'].non_field_errors())

        self.assertTemplateUsed(response, 'users/login.html')  # Should re-render the login page

    def test_logout_get(self):
        response = self.client.get(self.logout_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/logout.html')

    def test_logout_success(self):
        User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(self.logout_url)

        self.assertEqual(response.status_code, 200)  # Should render the logout page
        self.assertTemplateUsed(response, 'users/logout.html')

    def test_register_get(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_post_valid(self):
        # Create taxi locations for testing in the database
        for car_id in self.car_data['cars']:
            TaxiLocations.objects.create(date_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                         latitude="0.0", longitude="0.0", car_id=car_id)

        response = self.client.post(self.register_url, {**self.user_data, **self.car_data})

        # Clean up the database
        TaxiLocations.objects.filter(car_id__in=self.car_data['cars']).delete()

        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertTrue(User.objects.filter(username='testuser').exists())

        user = User.objects.get(username='testuser')
        # check if the cars are assigned to the user exists in the database
        self.assertTrue(Car.objects.filter(user=user, car_id='1').exists())
        self.assertTrue(Car.objects.filter(user=user, car_id='2').exists())

    def test_register_view_post_invalid_password_mismatch(self):
        self.user_data['password2'] = 'differentpassword'
        response = self.client.post(self.register_url, {**self.user_data, **self.car_data})
        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_register_view_post_car_already_assigned(self):
        # Create a car already assigned to another user
        existing_user = User.objects.create_user(username='existinguser', password='password123')
        Car.objects.create(user=existing_user, car_id='1')

        response = self.client.post(self.register_url, {**self.user_data, **self.car_data})
        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors
        self.assertFalse(User.objects.filter(username='testuser').exists())
