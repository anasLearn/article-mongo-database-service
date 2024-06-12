import os

from mongoengine import connect
from dotenv import load_dotenv

load_dotenv()
db_server_url = os.environ.get("DB_SERVER_URL")
db_name = os.environ.get("DB_NAME")

# Connect to the MongoDB instance
connect('dev-app-db', host=f'{db_server_url}/{db_name}')


def remove_duplicates(articles):
    # Check and remove duplicates from the list of articles
    unique_articles = []
    seen_titles = set()
    for article in articles:
        # Check if the article title is not in the set of seen titles
        if article['title'] not in seen_titles:
            # Add the article title to the set of seen titles
            seen_titles.add(article['title'])
            # Check if the article does not exist in the database
            if not article_exists_in_database(article):
                unique_articles.append(article)
    return unique_articles

def article_exists_in_database(article):
    # Check if the article exists in the database
    # Your database checking logic here
    # Return True if the article exists, False otherwise
    pass