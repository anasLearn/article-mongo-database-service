import json
from typing import List
from fastapi import FastAPI, HTTPException, Request
import uvicorn
from redis.asyncio import Redis
import redis.exceptions as redis_exceptions

from utils.worker_routine import run_worker_routine
from utils.db_utils import get_100_articles_from_db
from models.pydantic_models import (
    ArticleModel,
    convert_article_to_pydantic,
    custom_serializer,
)

import logging

from globals import HOST, PORT, UPDATE_DB_ENDPOINT, REDIS_HOST, REDIS_PORT
app = FastAPI()


# Initialize Redis connection
redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=7)


@app.get("/ping")
async def ping():
    return "Hello, DB microservice is alive"


# Create the /update_db endpoint
@app.get(f"/{UPDATE_DB_ENDPOINT}")
async def update_db(request: Request):
    """
    Update the contents of the article database from the newspaper websites.
    Only allowed if the requests is from the localhost

    Returns:
        dict: A message indicating the result of the update operation.
    """
    client_host = request.client.host
    if client_host != "127.0.0.1" and client_host != "localhost":
        raise HTTPException(status_code=403, detail="Access denied. Only local requests are allowed.")

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
async def get_100_articles(page: int = 1):
    try:
        # Check if articles are cached in Redis
        cache_key = f"articles_page_{page}"
        cached_articles = await redis_client.get(cache_key)  # Await the Redis operation

        if cached_articles:
            return json.loads(cached_articles)

    except redis_exceptions.ConnectionError:
        logging.error("Redis connection error.")
        raise HTTPException(status_code=500, detail="Error connecting to Redis.")

    except redis_exceptions.TimeoutError:
        logging.error("Redis timeout error.")
        raise HTTPException(status_code=500, detail="Redis request timed out.")

    except redis_exceptions.RedisError as e:
        logging.error(f"Redis error: {e}")
        raise HTTPException(status_code=500, detail="Error interacting with Redis.")

    try:
        articles = get_100_articles_from_db(page)

        # Serialize and cache the articles
        articles_list = [convert_article_to_pydantic(article) for article in articles]
        await redis_client.set(
            cache_key,
            json.dumps(
                [article.dict() for article in articles_list], default=custom_serializer
            ),
            ex=3600,  # Cache for 1 hour
        )

        return articles_list

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except LookupError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("api:app", host=HOST, port=PORT, reload=True)
