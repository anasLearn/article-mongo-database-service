import os

from mongoengine import connect, DoesNotExist
from dotenv import load_dotenv

from models import Article, Topic

load_dotenv()
db_server_url = os.environ.get("DB_SERVER_URL")
db_name = os.environ.get("DB_NAME")

# Connect to the MongoDB instance
connect(db_name, host=f'{db_server_url}/{db_name}')


def remove_db_duplicates(articles) -> list:
    """
    take as an input a dictionary of articles
    checks which of these articles already exist in the database
    return a list of articles url that doesn't contain the articles already existing in the database

    :param articles: dict
        {
            "article_1_url": {
                "img_url: "...",
                "source": "YLE or other",
                "topics": {"topic_1", "topic_2"}
            },
            "article_2_url": {
                "img_url: "...",
                "source": "YLE or other",
                "topics": {"topic_3", "topic_2"}
            },
            # and so on
        }

    :return:
    """
    # Check and remove duplicates from the list of articles
    unique_articles = []
    seen_titles = set()
    for article_url in articles:
        # Check if the article title is not in the set of seen titles
        if article_url not in seen_titles:
            # Add the article title to the set of seen titles
            seen_titles.add(article_url)
            # Check if the article does not exist in the database
            if not article_exists_in_database(article_url):
                unique_articles.append(article_url)
    return unique_articles


def article_exists_in_database(article_url):
    # Check if the article exists in the database
    # Your database checking logic here
    # Return True if the article exists, False otherwise
    return Article.objects(url=article_url).first() is not None


def write_to_database(article):
    # Write the article data to the database
    # Your database writing logic here
    Article(**article).save()
    # TODO: Deal with the case of an exception


def get_topic_by_name(topic_name):
    """
    Get a topic from the database by its name
    if it doesn't exist create it
    Args:
        topic_name:

    Returns:

    """
    try:
        topic = Topic.objects.get(name=topic_name)

    except DoesNotExist:
        topic = Topic(name=topic_name).save()

    return topic


def get_topics_dict(topics: set):
    """

    Args:
        topics:

    Returns:
        topics_dict = {
            "topic_name": topic_document_object
        }

    """
    topics_dict = {}
    for topic_name in topics:
        topics_dict[topic_name] = get_topic_by_name(topic_name)

    return topics_dict
