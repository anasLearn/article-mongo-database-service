import os

from dotenv import load_dotenv


load_dotenv()

HOST = os.environ.get("HOST", "localhost")
PORT = int(os.environ.get("PORT", "5030"))
UPDATE_DB_ENDPOINT = "update-db"
REDIS_HOST = os.environ.get("REDIS_HOST", "host.docker.internal")
REDIS_PORT = int(os.environ.get("REDIS_SERVER_URL", "6379"))
CELERY_FREQUENCY = os.environ.get("CELERY_FREQUENCY", "slow").lower().strip()
