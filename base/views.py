import mongoengine
from django.shortcuts import render
from django.conf import settings

from django.contrib.auth.decorators import login_required
from bson.json_util import dumps
from taxi_tracker.models import TaxiLocations, Car


@login_required
def map_view(request):
    mongoengine.register_connection(alias='core', name='taxi-tracker')
    # Filter cars and taxi locations by user to prevent unauthorized access
    cars_list = list(Car.objects.filter(user_id=request.user.id).values())
    car_ids_for_user = [car['car_id'] for car in cars_list]

    taxi_locations = TaxiLocations.objects.filter(car_id__in=car_ids_for_user)
    taxi_locations_json = dumps(taxi_locations.to_json())
    context = {
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        'taxi_locations': taxi_locations_json,
        'car_ids': car_ids_for_user,
        'user_id': request.user.id,
    }
    return render(request, 'base/map_view.html', context)
