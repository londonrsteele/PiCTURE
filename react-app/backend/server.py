# Filename : server.py
# Author   : LR Steele
# Descrptn : Flask server for React app
from flask import Flask
import datetime
import subprocess

# Initialize app
app = Flask(__name__)

# One route for api
@app.route("/home")
def say_hello():
    # return an api
    return {
        "Greeting": "Hello, ",
        "Name": "London!"
    }

# One route for api
@app.route("/time")
def give_time():
    now = datetime.datetime.now()
    # return an api
    return {
        "dow": now.strftime("%A"),
        "month": now.strftime("%B"),
        "date": now.strftime("%d"),
        "year": now.strftime("%Y"),
        "time": now.strftime("%I:%M"),
        "ampm": now.strftime("%p")
    }

# One route for api
@app.route("/wifi")
def give_wifi():
    wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
    data = wifi.decode('utf-8')
    if "GoStarsCTX" in data:
        return_msg = "Connected: GoStarsCTX"
    else:
        return_msg = "Not Connected :("
    return {
        "wifi": return_msg
    }

# One route for api
@app.route("/updated")
def give_updated():
    now = datetime.datetime.now()
    # return an api
    return {
        "time": now.strftime("%I:%M%p")
    }


































# Running app
if __name__ == "__main__":
    app.run(debug=True)