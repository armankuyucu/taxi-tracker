import mongoengine
from django.shortcuts import render
from django.conf import settings

from django.contrib.auth.decorators import login_required
import csv

import base.data_service as data_service

from base.cars import Cars
from bson.json_util import dumps


@login_required
def home(request):
    mongoengine.register_connection(alias='core', name='yazlab2_proje1')
    dataDictionary = dumps(Cars.objects.to_json())

    context = {
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        'mydata': dataDictionary,
        'user_id': request.user.id,
    }
    return render(request, 'base/home.html', context)


def csvParse():
    mongoengine.register_connection(alias='core', name='yazlab2_proje1')

    with open('static/cars.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if line[3] == "34" or line[3] == "386":
                # musteri1
                data_service.create_cars(line[0], float(line[1]), float(line[2]), int(line[3]), 2)
            elif line[3] == "292" or line[3] == "246":
                # musteri2
                data_service.create_cars(line[0], float(line[1]), float(line[2]), int(line[3]), 3)


# csvParse()
