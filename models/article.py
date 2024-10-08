from mongoengine import (
    Document,
    URLField,
    StringField,
    ReferenceField,
    ListField,
    DateTimeField,
    DictField
)
from .topic import Topic
from .newspaper import Newspaper
from .location import Country, Region, City


class Article(Document):
    meta = {"collection": "articles"}
    url = URLField(required=True)
    img_url = URLField()
    timestamp = DateTimeField(required=True)
    title = StringField()
    topics = ListField(ReferenceField(Topic), required=True)
    country = ReferenceField(Country, required=False)
    region = ReferenceField(Region, required=False)
    city = ReferenceField(City, required=False)
    # TODO: source = ReferenceField(Newspaper, required=True)
    source = StringField(required=True)
    summary = DictField(required=True)

    # Define indexes
    meta["indexes"] = [
        {
            "fields": ["url"],
            "unique": True,  # Create a unique index on the 'title' field
        }
    ]
