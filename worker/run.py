from worker.get_articles import get_latest_articles, scrap_article
from worker.db_utils import remove_db_duplicates, write_to_database
from worker.summarize_article import summarize_article
from worker.format_datetime import format_timestamp


def run_worker_routine():
    # Get the latest articles
    articles = get_latest_articles()
    if articles:
        # Remove duplicates
        # Unique articles are a list of article URLs
        unique_articles = remove_db_duplicates(articles)
        for article_url in unique_articles:
            # Scrap each article
            news_source = articles[article_url]["source"]
            scraped_article = scrap_article(article_url, news_source)
            if scraped_article:
                title = scraped_article["article_title"]
                intro = scraped_article["article_introduction"]
                content = scraped_article["article_content"]
                timestamp = format_timestamp(scraped_article["article_datetime"])
                topics = articles[article_url]["topics"]
                img_url = articles[article_url]["img_url"]

                # Summarize the content
                full_text = title + "\n\n" + intro + "\n\n" + content
                summary = summarize_article(full_text)

                if summary:
                    # Format the article data
                    formatted_article = {
                        'url': article_url,
                        'img_url': img_url,
                        'timestamp': timestamp,
                        'title': title,
                        'topics': topics,
                        'source': news_source,
                        'summary': summary
                    }
                    # Write to the database
                    write_to_database(formatted_article)
    else:
        # TODO: logging and exception
        # print("Failed to fetch latest articles")
        pass


if __name__ == "__main__":
    # Example usage
    run_worker_routine()
