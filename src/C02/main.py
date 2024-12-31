from flask import Flask

app = Flask(__name__)

@app.route("/login")
def login():
    return "<p>Hello, Bahman! We just sent you an OTP.</p>"