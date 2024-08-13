# Critical:

* Put the `requests.get` in `try - except` blocks
* Manage the exceptions when the articles scraper and the article summarizer are offline.
* each article must have the source as a Reference to the collection NewsPaper instead of a str

# Other:

* Make sure that scraping articles happen with a delay to respect the news website
* check that the number of articles saved in the database is equal to the number of articles in the RSS feed
* Check that the removal of duplicates that already exist in the database is working properly
* Make the access to the mongo database asynchronous. Hint:
  ```Python
    from motor.motor_asyncio import AsyncIOMotorClient
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['your_database']
    article_collection = db['articles']
    
    async def get_100_articles_from_db(page: int):
        skip = (page - 1) * 100
        cursor = article_collection.find().sort('timestamp', -1).skip(skip).limit(100)
        articles = await cursor.to_list(length=100)
        return articles
   ```
* If that's not possible, make the update of the redis cache by reading the database subject to thread lock.
  * The objective is that only one client can update the redis cache with only one access to the database.
* clear the redis cache after updating the database
* Make an endpoint for the topics
* Remove the possibility to update the database with the API. or at least secure it.
