import random

from utils.get_articles import get_latest_articles, get_scraped_article
from utils.db_utils import remove_db_duplicates, write_to_database, get_topics_dict
from utils.summarize_article import summarize_article
from utils.format_datetime import format_timestamp
from globals import CELERY_FREQUENCY


def run_worker_routine():
    # Get the latest articles
    scraped_articles, scraped_topics = get_latest_articles()
    topics_dict = get_topics_dict(scraped_topics)
    if scraped_articles:
        # Remove duplicates
        # Unique articles are a list of article URLs
        unique_articles = remove_db_duplicates(scraped_articles)

        if CELERY_FREQUENCY == "quick":
            unique_articles = random.choices(unique_articles, k=5)
            
        for article_url in unique_articles:
            # Scrap each article
            news_source = scraped_articles[article_url]["source"]
            scraped_article = get_scraped_article(article_url, news_source)
            if scraped_article:
                title = scraped_article["article_title"]
                intro = scraped_article["article_introduction"]
                content = scraped_article["article_content"]
                timestamp = format_timestamp(scraped_article["article_datetime"])
                topics_str_list = scraped_articles[article_url]["topics"]
                topics = [topics_dict[topic] for topic in topics_str_list]
                img_url = scraped_articles[article_url]["img_url"]

                # Summarize the content
                full_text = title + "\n\n" + intro + "\n\n" + content
                summary = summarize_article(full_text)

                if summary:
                    # Format the article data
                    formatted_article = {
                        "url": article_url,
                        "img_url": img_url,
                        "timestamp": timestamp,
                        "title": title,
                        "topics": topics,
                        "source": news_source,
                        "summary": summary,
                    }
                    # Write to the database
                    write_to_database(formatted_article)

        return "Database update completed"
    else:
        # TODO: logging and exception
        # print("Failed to fetch latest articles")
        pass


if __name__ == "__main__":
    # Example usage
    run_worker_routine()
