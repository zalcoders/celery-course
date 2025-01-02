from celery import Celery
from celery.schedules import crontab



app = Celery("tasks", backend="redis://localhost:6379/0", include=["background_jobs.tasks"])

app.conf.broker_url = "redis://localhost:6379/0"


app.conf.beat_schedule = {
    'ping-every-day-at-8-am': {
        'task': 'background_jobs.tasks.ping',
        'schedule': crontab(hour=8, minute=0),
        'args': (1, )
    },
}