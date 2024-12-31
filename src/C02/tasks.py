from celery import Celery
import time

app = Celery("tasks", backend="redis://localhost:6379/0")

app.conf.broker_url = "redis://localhost:6379/0"

@app.task
def send_otp(phone_no, otp):
    time.sleep(5)
    return True

@app.task
def custom_exception():
    raise Exception("ZalCoders")
    return True