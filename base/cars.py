import mongoengine
from mongoengine import Document


class Cars(Document):
    date_time = mongoengine.StringField(required=True)
    latitude = mongoengine.FloatField(required=True)
    longitude = mongoengine.FloatField(required=True)
    car_id = mongoengine.IntField(required=True)
    user_id = mongoengine.IntField(required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'cars'
    }

