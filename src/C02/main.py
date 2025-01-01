from flask import Flask
from background_jobs.tasks import send_otp

app = Flask(__name__)

@app.route("/login")
def login():
    send_otp.delay(4, 4)
    return "<p>Hello, Bahman! We just sent you an OTP.</p>"