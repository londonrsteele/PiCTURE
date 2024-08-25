# Filename : server.py
# Author   : LR Steele
# Descrptn : Flask server for React app
#########################################################################################
# Flask imports
from urllib import response
from flask import Flask, jsonify
import datetime
import subprocess
import os.path
import requests
# Google Calendar imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
# Weather imports
import openmeteo_requests
import requests_cache
from retry_requests import retry
import json

#########################################################################################
# Initialize app
#########################################################################################
app = Flask(__name__)

#########################################################################################
# One route for api - /time
#########################################################################################
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

#########################################################################################
# One route for api - /quote
#########################################################################################
@app.route("/quote")
def give_quote():
    quote_api_url = "https://zenquotes.io/api/quotes"
    response = requests.get(quote_api_url).json()
    return response

#########################################################################################
# One route for api - /wifi
#########################################################################################
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

#########################################################################################
# One route for api - /updated
#########################################################################################
@app.route("/updated")
def give_updated():
    now = datetime.datetime.now()
    # return an api
    return {
        "time": now.strftime("%I:%M%p")
    }

#########################################################################################
# One route for api - /calendar
#########################################################################################
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

#########################################################################################
# One route for api - /weather
#########################################################################################
@app.route("/weather")
def give_weather():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	    "latitude": 31.1171,
	    "longitude": -97.7278,
	    "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "weather_code", "cloud_cover", "wind_speed_10m"],
	    "daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "daylight_duration"],
	    "temperature_unit": "fahrenheit",
	    "wind_speed_unit": "mph",
	    "precipitation_unit": "inch",
	    "timezone": "America/Chicago"
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    json_response = {
        "latitude": response.Latitude(),
        "longitude": response.Longitude(),
        "current": [
            {"temperature": response.Current().Variables(0).Value()},
            {"relative_humidity": response.Current().Variables(1).Value()},
            {"feels_like_temp": response.Current().Variables(2).Value()},
            {"day_or_night": response.Current().Variables(3).Value()},
            {"precipitation": response.Current().Variables(4).Value()},
            {"weather_code": response.Current().Variables(5).Value()},
            {"cloud_cover": response.Current().Variables(6).Value()},
            {"wind_speed": response.Current().Variables(7).Value()}
        ],
        "daily": [
            {"max_temp": response.Daily().Variables(0).Value()},
            {"min_temp": response.Daily().Variables(1).Value()},
            {"sunrise": response.Daily().Variables(2).Value()},
            {"sunset": response.Daily().Variables(3).Value()},
            {"daylight_duration": response.Daily().Variables(4).Value()}
        ]
    }
    return json.dumps(json_response)



#########################################################################################
# Running app
#########################################################################################
if __name__ == "__main__":
    app.run(debug=True)