from time import sleep

from background_jobs.celery import app
from celery.schedules import crontab


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, ping.s(1), name="Ping Command Every 10 Seconds")


@app.task
def ping(wait_time):
    sleep(wait_time)
    return "pong"