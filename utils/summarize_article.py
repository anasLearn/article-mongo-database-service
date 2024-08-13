import os
import requests
from dotenv import load_dotenv

load_dotenv()
summarizer_address = os.environ.get("SUMMARIZER_URL")
summarize_endpoint = os.environ.get("SUMMARIZE_ENDPOINT")
SAMPLE_SUMMARY = not (
    "false" == os.environ.get("SAMPLE_SUMMARY", default="true").lower().strip()
)


def summarize_article(content):
    if SAMPLE_SUMMARY:
        return "A sample summary"
    # Summarize an article using article-summary-service
    response = requests.post(
        f"{summarizer_address}/{summarize_endpoint}", json={"content": content}
    )
    if response.status_code == 200:
        return response.json()
    else:
        # TODO: logging and exception
        return None
