import time
from background_jobs.celery import app


@app.task
def send_otp(phone_no, otp):
    time.sleep(5)
    return True

@app.task
def custom_exception():
    raise Exception("ZalCoders")
    return True