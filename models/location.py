from mongoengine import Document, StringField, ReferenceField


# Country Document
class Country(Document):
    meta = {'collection': 'countries'}
    name = StringField(required=True)


# Region Document
class Region(Document):
    meta = {'collection': 'regions'}
    name = StringField(required=True)
    country = ReferenceField(Country, required=True)


# City Document
class City(Document):
    meta = {'collection': 'cities'}
    name = StringField(required=True)
    country = ReferenceField(Country, required=True)
    region = ReferenceField(Region, required=False)
