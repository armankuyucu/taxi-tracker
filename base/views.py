import mongoengine
from django.shortcuts import render
from django.conf import settings

from django.contrib.auth.decorators import login_required
import csv

from base import mongodb_setup as mongodb_setup
import base.data_service as data_service

# mongodb_setup.global_init()
from base.cars import Cars
# from json import dumps
from bson.json_util import loads, dumps


@login_required
def home(request):
    mongoengine.register_connection(alias='core', name='yazlab2_proje1')
    dataDictionary = {}
    # for car in Cars.objects:
    #     dataDictionary += car

    dataDictionary = dumps(Cars.objects.to_json())
    # print(dataDictionary)
    context = {
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        "mydata": dataDictionary
    }
    print(context)
    return render(request, 'base/home.html', context)


def csvParse():
    with open('static/cars.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        counter = 0
        for line in csv_reader:
            if counter <= 1439:
                # musteri1
                data_service.create_cars(line[0], float(line[1]), float(line[2]), int(line[3]), 2)
            elif 1440 <= counter:
                # musteri2
                data_service.create_cars(line[0], float(line[1]), float(line[2]), int(line[3]), 3)

            counter += 1

# csvParse()
