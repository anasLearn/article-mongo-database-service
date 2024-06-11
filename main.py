from datetime import datetime
from mongoengine import connect
from models import Topic, Article
from models.location import Country, Region, City
from models.newspaper import Newspaper



# Connect to the MongoDB instance
connect('dev-app-db', host='mongodb://localhost:27017/dev-db')

# Example usage
if __name__ == "__main__":
    # Creating Topics
    tech_topic = Topic(name="Technology")
    tech_topic.save()

    science_topic = Topic(name="Science")
    science_topic.save()

    sport_topic = Topic(name="Sport")
    sport_topic.save()

    # Create a country
    country = Country(name="Finland")
    country.save()

    # Create a region
    region = Region(name="Uusimaa", country=country)
    region.save()

    # Create a city
    city = City(name="Helsinki", country=country, region=region)
    city.save()

    # Create a newspaper
    newspaper = Newspaper(name="YLE", root_url="https://yle.fi/")
    newspaper.save()

    # Creating an Article with multiple topics
    article = Article(
        url="https://yle.fi/a/74-20093256",
        img="https://images.cdn.yle.fi/image/upload/ar_1.4997854997854998,c_fill,g_faces,h_424,w_636/dpr_1.0/q_auto:eco/f_auto/fl_lossy/v1718086047/39-13009466667e9837a20d",
        topics=[sport_topic],
        country=country,
        source=newspaper,
        summary="This is a summary of the article.",
        timestamp=datetime.now()
    )
    article.save()

    # Querying the Article
    fetched_article = Article.objects.first()
    print(fetched_article.url)
    for topic in fetched_article.topics:
        print(topic.name)
