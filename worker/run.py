import requests
from .get_articles import get_latest_articles




def scrap_article(article):
    # Scrap an article using article-scraper-service
    response = requests.post("http://article-scraper-service/scrap_article", json=article)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def summarize_article(content):
    # Summarize an article using article-summary-service
    response = requests.post("http://article-summary-service/summarize_article", json={"content": content})
    if response.status_code == 200:
        return response.json()['summary']
    else:
        return None

def run_worker_routine():
    # Get the latest articles
    articles = get_latest_articles()
    if articles:
        # Remove duplicates
        unique_articles = remove_duplicates(articles)
        for article in unique_articles:
            # Scrap each article
            scraped_data = scrap_article(article)
            if scraped_data:
                # Summarize the content
                summary = summarize_article(scraped_data['content'])
                if summary:
                    # Format the article data
                    formatted_article = {
                        'title': article['title'],
                        'content': scraped_data['content'],
                        'summary': summary,
                        'image_url': scraped_data['image_url'],
                        'topic': scraped_data['topic']
                    }
                    # Write to the database
                    write_to_database(formatted_article)
    else:
        print("Failed to fetch latest articles")

def write_to_database(article):
    # Write the article data to the database
    # Your database writing logic here
    pass

# Example usage
run_worker_routine()
