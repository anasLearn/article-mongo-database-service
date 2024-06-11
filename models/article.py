from mongoengine import Document, URLField, StringField, ReferenceField, ListField, DateTimeField
from .topic import Topic
from .newspaper import Newspaper
from .location import Country, Region, City


class Article(Document):
    meta = {'collection': 'articles'}
    url = URLField(required=True)
    img = URLField()
    timestamp = DateTimeField(required=True)
    topics = ListField(ReferenceField(Topic), required=True)
    country = ReferenceField(Country, required=True)
    region = ReferenceField(Region, required=False)
    city = ReferenceField(City, required=False)
    source = ReferenceField(Newspaper, required=True)
    summary = StringField()

    # Define indexes
    meta['indexes'] = [
        {
            'fields': ['url'], 'unique': True  # Create a unique index on the 'title' field
        }
    ]


