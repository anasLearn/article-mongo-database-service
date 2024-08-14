import os

from dotenv import load_dotenv


load_dotenv()

HOST = os.environ.get("HOST", "localhost")
PORT = int(os.environ.get("PORT", "5030"))
UPDATE_DB_ENDPOINT = "update-db"