from mongoengine import Document, URLField, StringField, ReferenceField
from .topic import Topic


class Article(Document):
    meta = {'collection': 'articles'}
    url = URLField(required=True)
    img = URLField()
    summary = StringField()
    topic = ReferenceField(Topic, required=True)
