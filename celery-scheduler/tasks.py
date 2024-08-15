from celery import Celery
from celery.schedules import crontab
import requests
import logging

from globals import HOST, PORT, UPDATE_DB_ENDPOINT, REDIS_HOST, REDIS_PORT, CELERY_FREQUENCY


# Create Celery instance
app = Celery("tasks", broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0", backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/1")


@app.task
def run_worker():
    logging.warning("Worker is starting: Updating DB")
    response = requests.get(f"http://{HOST}:{PORT}/{UPDATE_DB_ENDPOINT}")
    if response.status_code == 200:
        logging.warning("DB Update completed!")
    else:
        logging.error("DB Update Error.")


if CELERY_FREQUENCY == "quick":
    # # Schedule the task to run every 5 minutes
    # app.conf.beat_schedule = {
    #     'run-worker-every-5-minutes': {
    #         'task': 'celery-scheduler.tasks.run_worker',
    #         'schedule': crontab(minute='*/5'),  # Run at minute 0, 5, 10, 15, etc. of every hour
    #     },
    # }

    # Schedule the task to run every 2 minutes
    app.conf.beat_schedule = {
        'run-worker-every-2-minutes': {
            'task': 'celery-scheduler.tasks.run_worker',
            'schedule': crontab(minute='*/2'),  # Run at minute 0, 2, 4, 6, etc. of every hour
        },
    }

else:
    # Schedule the task to run every 4 hours
    app.conf.beat_schedule = {
        "run-worker-every-4-hours": {
            "task": "celery-scheduler.tasks.run_worker",
            "schedule": crontab(
                minute=0, hour="*/4"
            ),  # Run at minute 0 of every 4th hour (0, 4, 8, 12, 16, 20)
        },
    }

app.conf.timezone = "Europe/Paris"
