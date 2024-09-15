# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from taxi_tracker.models import TaxiLocations


class CustomUserCreationForm(UserCreationForm):
    unique_car_ids = TaxiLocations.objects.distinct(field="car_id")

    cars = forms.MultipleChoiceField(
        choices=[(car_id, str(car_id)) for car_id in unique_car_ids],
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select your cars"
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'cars']

    def __init__(self, *args, **kwargs):
        # This ensures that the choices are populated when the form is instantiated
        super().__init__(*args, **kwargs)
        unique_car_ids = TaxiLocations.objects.distinct(field="car_id")
        self.fields['cars'].choices = [(car_id, str(car_id)) for car_id in unique_car_ids]
        