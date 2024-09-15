# base/tests/test_functional.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from mongoengine import connect, disconnect
from taxi_tracker.data_service import populate_database
from taxi_tracker.models import TaxiLocations, Car
from datetime import datetime
import time


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        disconnect(alias='core')
        connect('taxi_tracker_test', alias='core')
        populate_database('taxi_tracker_test')
        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        self.register_url = self.live_server_url + reverse('register')
        self.login_url = self.live_server_url + reverse('login')
        self.map_view_url = self.live_server_url + reverse('map_view')

        self.user_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        self.car_data = {
            'cars': TaxiLocations.objects.distinct('car_id')
        }

        # Create taxi locations for testing in the database
        for car_id in self.car_data['cars']:
            TaxiLocations.objects.create(date_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                         latitude="0.0", longitude="0.0", car_id=car_id)

    def tearDown(self):
        self.browser.close()
        # delete all taxi locations
        TaxiLocations.objects.all().delete()
        disconnect(alias='core')

    def test_user_registration_login_and_map_view_access(self):
        time.sleep(2)
        # Register the user
        self.browser.get(self.register_url)
        time.sleep(2)
        self.browser.find_element(By.NAME, 'username').send_keys(self.user_data['username'])
        time.sleep(2)
        self.browser.find_element(By.NAME, 'password1').send_keys(self.user_data['password1'])
        time.sleep(2)
        self.browser.find_element(By.NAME, 'password2').send_keys(self.user_data['password2'])
        time.sleep(2)
        # Select the checkboxes for the cars
        for car_id in self.car_data['cars'][:2]:
            checkbox = self.browser.find_element(By.CSS_SELECTOR, f"input[name='cars'][value='{car_id}']")
            if not checkbox.is_selected():
                checkbox.click()
        time.sleep(2)
        # get by its type which is submit
        self.browser.find_element(By.NAME, 'Sign Up').click()
        time.sleep(2)
        # Log in the user
        self.browser.get(self.login_url)
        time.sleep(2)
        self.browser.find_element(By.NAME, 'username').send_keys(self.user_data['username'])
        time.sleep(2)
        self.browser.find_element(By.NAME, 'password').send_keys(self.user_data['password1'])
        time.sleep(2)
        self.browser.find_element(By.NAME, 'Login').click()
        time.sleep(2)
        # Access the map view
        self.browser.get(self.map_view_url)
        time.sleep(2)
        self.assertIn('Taxi Tracker', self.browser.title)
        self.assertTemplateUsed('base/map_view.html')

        # Check if the cars are assigned to the user
        user = User.objects.get(username='testuser')
        self.assertTrue(Car.objects.filter(user=user, car_id=str(self.car_data['cars'][0])).exists())
        self.assertTrue(Car.objects.filter(user=user, car_id=str(self.car_data['cars'][1])).exists())
        
        # Check if the last 30 minutes of taxi locations are displayed
        time.sleep(10)

        # Select first car from the dropdown
        select = Select(self.browser.find_element(By.ID, 'car-select'))
        select.select_by_value(str(self.car_data['cars'][0]))

        time.sleep(2)
        # Select time range 8AM to 20PM from the dropdown
        # clear startHour and endHour first
        self.browser.find_element(By.ID, 'startHour').clear()
        self.browser.find_element(By.ID, 'endHour').clear()
        self.browser.find_element(By.ID, 'startHour').send_keys('8')
        self.browser.find_element(By.ID, 'endHour').send_keys('20')

        # submit the form
        self.browser.find_element(By.ID, 'submit').click()
        time.sleep(10)
