from celery import Celery
import time

app = Celery("tasks", broker="redis://localhost:6379/0")

@app.task
def send_otp(phone_no, otp):
    time.sleep(5)
    return True