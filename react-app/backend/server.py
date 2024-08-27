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
from dotenv import load_dotenv, dotenv_values
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
import numpy
from functools import reduce
import math

#########################################################################################
# Initialize app
#########################################################################################
load_dotenv()
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
                calendarId=os.getenv("ALEX_AND_LONDON_CALID"),
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
                date = str(date_object.strftime("%b %d, %Y"))
                day = str(date_object.strftime("%A"))

            
            # for all-day events
            else:
                start = "All Day"
                end = "All Night"

                event_date = event["start"].get("date")
                date_format = "%Y-%m-%d"
                date_object = datetime.datetime.strptime(event_date, date_format)
                day = str(date_object.strftime("%A"))
                date = str(date_object.strftime("%b %d, %Y"))

            # Check if date == Today
            today = str(datetime.datetime.now().strftime("%b %d, %Y"))
            if date == today:
                date = "Today"

            event_dict = {
                "day": day,
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
    
    return weather_helper(response)

def weather_helper(response):
    # Current variables
    if int(response.Current().Variables(3).Value()) == 1:
        day_or_night = "day"
    else:
        day_or_night = "night"

    # Daily variables
    max_temp = int(response.Daily().Variables(0).ValuesAsNumpy()[0])
    min_temp = int(response.Daily().Variables(1).ValuesAsNumpy()[0])
    sun_format = "%Y-%m-%dT%H:%M:%S"
    sunrise_str = datetime.datetime.fromtimestamp(response.Daily().Variables(2).ValuesInt64(0)).isoformat()
    sunrise_object = datetime.datetime.strptime(sunrise_str, sun_format)
    sunrise = sunrise_object.strftime("%I:%M %p")
    sunset_str = datetime.datetime.fromtimestamp(response.Daily().Variables(3).ValuesInt64(0)).isoformat()
    sunset_object = datetime.datetime.strptime(sunset_str, sun_format)
    sunset = sunset_object.strftime("%I:%M %p")
    daylight_duration_sec = int(response.Daily().Variables(4).ValuesAsNumpy()[0])
    daylight_duration_hrs = int(math.floor(daylight_duration_sec / 60 / 60))
    daylight_duration_min = int(round(daylight_duration_sec / 60 % 60, 0))

    # Pass Current and Daily Weather Codes
    weather_code = weathercode_helper(int(response.Current().Variables(5).Value()), day_or_night)
    # Create dict to jsonify
    json_response = {
        "current": [
            {"temperature": int(response.Current().Variables(0).Value())},
            {"relative_humidity": int(response.Current().Variables(1).Value())},
            {"feels_like_temp": int(response.Current().Variables(2).Value())},
            {"day_or_night": day_or_night},
            {"precipitation": response.Current().Variables(4).Value()},
            {"weather_code_str": weather_code["string"]},
            {"weather_code_icon": weather_code["icon"]},
            {"cloud_cover": int(response.Current().Variables(6).Value())},
            {"wind_speed": int(response.Current().Variables(7).Value())}
        ],
        "daily": [
            {"max_temp": max_temp},
            {"min_temp": min_temp},
            {"sunrise": sunrise},
            {"sunset": sunset},
            {"daylight_duration_hrs": daylight_duration_hrs},
            {"daylight_duration_min": daylight_duration_min}
        ]
    }
    return json.dumps(json_response)

def weathercode_helper(weather_code, day_or_night):
    weather_string_and_icon = {}

    match weather_code:
        case 0 | 1: 
            weather_string_and_icon["string"] = "Clear sky"
            if day_or_night == "day":
                weather_string_and_icon["icon"] = "ClearSkyDay.svg"
            else:
                weather_string_and_icon["icon"] = "ClearSkyNight.svg"
        case 2:
            weather_string_and_icon["string"] = "Partly cloudy"
            if day_or_night == "day":
                weather_string_and_icon["icon"] = "PartlyCloudyDay.svg"
            else:
                weather_string_and_icon["icon"] = "PartlyCloudyNight.svg"
        case 3:
            weather_string_and_icon["string"] = "Overcast"
            weather_string_and_icon["icon"] = "Cloudy.svg"
        case 45 | 48:
            weather_string_and_icon["string"] = "Foggy"
            weather_string_and_icon["icon"] = "Fog.svg"
        case 51 | 53 | 55:
            weather_string_and_icon["string"] = "Drizzle"
            weather_string_and_icon["icon"] = "Drizzle.svg"
        case 56 | 57:
            weather_string_and_icon["string"] = "Freezing drizzle"
            weather_string_and_icon["icon"] = "FreezingRain.svg"
        case 61 | 63 | 80 | 81:
            weather_string_and_icon["string"] = "Rain"
            weather_string_and_icon["icon"] = "Rain.svg"
        case 65 | 82:
            weather_string_and_icon["string"] = "Heavy rain"
            weather_string_and_icon["icon"] = "RainHeavy.svg"
        case 66 | 67:
            weather_string_and_icon["string"] = "Freezing rain"
            weather_string_and_icon["icon"] = "FreezingRainHeavy.svg"
        case 71 | 73 | 75 | 77 | 85 | 86: 
            weather_string_and_icon["string"] = "Snow"
            weather_string_and_icon["icon"] = "Snow.svg"
        case 95:
            weather_string_and_icon["string"] = "Thunderstorm"
            weather_string_and_icon["icon"] = "Thunderstorm.svg"
        case _:
            weather_string_and_icon["string"] = str("Error: Weather Code "+str(weather_code))
            weather_string_and_icon["icon"] = str("Error: Weather Code "+str(weather_code))

    return weather_string_and_icon

#########################################################################################
# Running app
#########################################################################################
if __name__ == "__main__":
    app.run(debug=True)

    