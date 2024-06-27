from mongoengine import Document, StringField


class Topic(Document):
    meta = {"collection": "topics"}
    name = StringField(required=True)
