from mongoengine import connect, Document, StringField, URLField, ReferenceField

# Connect to a remote MongoDB instance
connect('myappdatabase', host='mongodb://remote_host:27017/remotedatabase')

# Define the Topic model
class Topic(Document):
    meta = {'collection': 'topics'}
    name = StringField(required=True)

# Define the Article model
class Article(Document):
    meta = {'collection': 'articles'}
    url = URLField(required=True)
    img = URLField()
    summary = StringField()
    topic = ReferenceField(Topic, required=True)

# Example Usage
if __name__ == "__main__":
    # Creating a Topic
    tech_topic = Topic(name="Technology")
    tech_topic.save()

    # Creating an Article
    article = Article(
        url="https://example.com/article1",
        img="https://example.com/image1.jpg",
        summary="This is a summary of the article.",
        topic=tech_topic
    )
    article.save()

    # Querying the Article
    fetched_article = Article.objects.first()
    print(fetched_article.url, fetched_article.topic.name)
