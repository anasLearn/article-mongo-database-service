from mongoengine import connect
from models import Topic, Article

# Connect to the MongoDB instance
connect('dev-app-db', host='mongodb://localhost:27017/dev-db')

# Example usage
if __name__ == "__main__":
    # Creating a Topic
    tech_topic = Topic(name="Science")
    tech_topic.save()

    # Creating an Article
    article = Article(
        url="https://example.com/article2",
        img="https://example.com/image2.jpg",
        summary="This is a summary of the article.",
        topic=tech_topic
    )
    article.save()

    # Querying the Article
    fetched_article = Article.objects.first()
    print(fetched_article.url, fetched_article.topic.name)
