import json
import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import uvicorn
from redis import Redis

from worker.db_utils import get_100_articles_from_db
from worker.run import run_worker_routine
from models.pydantic_models import ArticleModel

import logging

load_dotenv()
app = FastAPI()
HOST = os.environ.get("HOST", "localhost")
PORT = int(os.environ.get("PORT", "5030"))


# Initialize Redis connection
redis_client = Redis(host="localhost", port=6379, db=0)


@app.get("/ping")
async def ping():
    return "Hello, DB microservice is alive"


# Create the /update_db endpoint
@app.post("/update-db")
def update_db():
    """
    Update the contents of the article database from the newspaper websites

    Returns:

    """
    try:
        result = run_worker_routine()
        return {"message": result}

    except HTTPException as he:
        # Log the error and re-raise HTTP exceptions
        logging.error(f"HTTPException: {he.detail}")
        raise he
    except Exception as e:
        # Log unexpected errors and return a 500 status code
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Fetch articles with pagination
@app.get("/get-100-articles/", response_model=List[ArticleModel])
def get_100_articles(page: int = 1):
    # Check if articles are cached in Redis
    cache_key = f"articles_page_{page}"
    cached_articles = redis_client.get(cache_key)

    if cached_articles:
        return json.loads(cached_articles)

    try:
        articles = get_100_articles_from_db(page)

        # Serialize and cache the articles
        articles_list = [ArticleModel.model_validate(article) for article in articles]
        redis_client.set(
            cache_key, json.dumps([article.dict() for article in articles_list]), ex=3600
        )  # Cache for 1 hour

        return articles_list

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except LookupError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("api:app", host=HOST, port=PORT, reload=True)
