from mongoengine import Document, StringField


# Newspaper Document
class Newspaper(Document):
    meta = {"collection": "newspapers"}
    name = StringField(required=True)
    root_url = StringField(required=True)
