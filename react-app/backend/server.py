# Filename : server.py
# Author   : LR Steele
# Descrptn : Flask server for React app
import json
from flask import Flask, jsonify
import datetime
import subprocess
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

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

# One route for api
@app.route("/calendar")
def give_calendar():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                ".\\react-app\\backend\\credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=5,
                singleEvents=True,
                orderBy="startTime",
                timeZone="CST"
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return jsonify(items=[])

        # Prints the start and name of the next 10 events
        event_list = []
        for event in events:
            
            # For timed (not all-day) events
            event_start = event["start"].get("dateTime")
            if event_start:
                start_format = "%Y-%m-%dT%H:%M:%S%z"
                start_object = datetime.datetime.strptime(event_start, start_format)
                start = start_object.strftime("%I:%M %p")

                event_end = event["end"].get("dateTime")
                end_format = "%Y-%m-%dT%H:%M:%S%z"
                end_object = datetime.datetime.strptime(event_end, end_format)
                end = end_object.strftime("%I:%M %p")

                event_date = event["start"].get("dateTime")
                date_format = "%Y-%m-%dT%H:%M:%S%z"
                date_object = datetime.datetime.strptime(event_date, date_format)
                date = str(date_object.strftime("%a %b %d, %Y"))
            
            # for all-day events
            else:
                start = "All Day"
                end = "All Night"

                event_date = event["start"].get("date")
                date_format = "%Y-%m-%d"
                date_object = datetime.datetime.strptime(event_date, date_format)
                date = str(date_object.strftime("%a %b %d, %Y"))

            # Check if date == Today
            today = str(datetime.datetime.now().strftime("%a %b %d, %Y"))
            if date == today:
                date = "Today"

            event_dict = {
                "date": date,
                "start": start,
                "end": end,
                "summary": event["summary"]
            }

            event_list.append(event_dict)
        
        return jsonify(items=event_list)

    except HttpError as error:
        print(f"An error occurred: {error}")



































# Running app
if __name__ == "__main__":
    app.run(debug=True)