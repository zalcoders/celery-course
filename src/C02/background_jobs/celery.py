from celery import Celery


app = Celery("tasks", backend="redis://localhost:6379/0", include=["background_jobs.tasks"])

app.conf.broker_url = "redis://localhost:6379/0"
