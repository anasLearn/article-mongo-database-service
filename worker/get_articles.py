import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
scraper_url = os.environ.get("SCRAPER_URL")
get_articles_endpoint = os.environ.get("ARTICLES_LIST_ENDPOINT")
scrap_article_endpoint = os.environ.get("SCRAP_ARTICLE_ENDPOINT")
news_sources = json.loads(os.environ.get("NEWS_SOURCES"))


def get_latest_articles():
    """

    :return:
        all_articles = {
            "article_url": {
                "img_url: "...",
                "source": "YLE or other",
                "topics": {"topic_1", "topic_2"}
            }
        }
    """
    # Connect to article-scraper-service to get the latest articles
    all_articles = {}
    all_topics = set()
    for news_source in news_sources:
        response = requests.get(f"{scraper_url}/{get_articles_endpoint}?source={news_source}")
        if response.status_code == 200:
            articles_dict = dict(response.json())
            for source in articles_dict:
                for topic in articles_dict[source]:
                    for article in articles_dict[source][topic]:
                        article_url = article["url"]
                        article_img_url = article["img_url"]
                        if article_url in all_articles:
                            all_articles[article_url]["topics"].add(topic)
                        else:
                            all_articles[article_url] = {
                                "img_url": article_img_url,
                                "source": source,
                                "topics": {topic}
                            }
                    all_topics.add(topic.lower().strip())

        else:
            # TODO: log the problem and raise an exception if needed
            pass

    return all_articles, all_topics


def scrap_article(article_url, news_source):
    # Scrap an article using article-scraper-service
    payload = {
        "url": article_url
    }
    response = requests.post(f"{scraper_url}/{scrap_article_endpoint}?source={news_source}", json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        # TODO: logging and exception
        return None


if __name__ == "__main__":
    from pprint import pprint
    pprint(get_latest_articles())