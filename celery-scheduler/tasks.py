from celery import Celery
from celery.schedules import crontab
import requests
import logging

from globals import HOST, PORT, UPDATE_DB_ENDPOINT


# Create Celery instance
app = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/1")


@app.task
def run_worker():
    logging.warning("Worker is starting: Updating DB")
    response = requests.get(f"http://{HOST}:{PORT}/{UPDATE_DB_ENDPOINT}")
    if response.status_code == 200:
        logging.warning("DB Update completed!")
    else:
        logging.error("DB Update Error.")


# Schedule the task to run every 4 hours
app.conf.beat_schedule = {
    "run-worker-every-4-hours": {
        "task": "celery-scheduler.tasks.run_worker",
        "schedule": crontab(
            minute=0, hour="*/4"
        ),  # Run at minute 0 of every 4th hour (0, 4, 8, 12, 16, 20)
    },
}

# # Schedule the task to run every 2 minutes
# app.conf.beat_schedule = {
#     'run-worker-every-2-minutes': {
#         'task': 'celery-scheduler.tasks.run_worker',
#         'schedule': crontab(minute='*/2'),  # Run at minute 0, 2, 4, 6, etc. of every hour
#     },
# }

app.conf.timezone = "Europe/Paris"
