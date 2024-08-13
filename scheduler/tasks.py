from celery import Celery
from celery.schedules import crontab

from scheduler.worker_routine import run_worker_routine

import logging

# Create Celery instance
app = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/1")


@app.task
def run_worker():
    run_worker_routine()
    logging.warning("Worker is running!")


# Schedule the task to run every 4 hours
app.conf.beat_schedule = {
    "run-worker-every-4-hours": {
        "task": "scheduler.tasks.run_worker",
        "schedule": crontab(
            minute=0, hour="*/4"
        ),  # Run at minute 0 of every 4th hour (0, 4, 8, 12, 16, 20)
    },
}

app.conf.timezone = "Europe/Paris"
