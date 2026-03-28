import os
import requests
from twilio.rest import Client

# Twilio account settings to send SMS
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

# Openweathermap params to get weather forecast
Endpoint = "http://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")
MY_LAT = 44.318378
MY_LONG = 23.796400

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "cnt": 4
}

# Another way to make a request: Endpoint and params with separate arguments
# Get weather report every 3 hours for the next 12 hours
response = requests.get(Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

condition_codes = []
for items in weather_data["list"]:
   condition_codes.append(items["weather"][0]["id"])

# If any weather report shows "rain" (condition code < 700) send an SMS or WhatsApp
if any(x < 700 for x in condition_codes):
    client = Client(account_sid, auth_token)

    # Send WhatsApp to personal phone
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body="It's going to rain today, remember to bring an ☂️",
        to='whatsapp:+16506693642'
    )
