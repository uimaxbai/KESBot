import os
import json
import requests
weather_token = os.environ['WEATHER_API_KEY']
place = input("> ")
response = requests.request("GET", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/london?unitGroup=metric&include=days&key=52ZZPYY6U92CNSYCA5PFC7872&contentType=json")
print(response)
jsonData = response.json()
address = jsonData["resolvedAddress"]
desc = jsonData["days"][0]["description"]
title = f"Weather in {address}"
temp = jsonData["days"][0]["temp"]
tempmax = jsonData["days"][0]["tempmax"]
tempmin = jsonData["days"][0]["tempmin"]
feelslike = jsonData["days"][0]["feelslike"]
percip = jsonData["days"][0]["precipprob"]
cond = jsonData["days"][0]["conditions"]
sunset = jsonData["days"][0]["sunset"]
sunrise = jsonData["days"][0]["sunrise"]
print(f"Weather today: {cond} with a {percip}% chance of rain. Highs at {tempmax} degrees Celcius with a low of {tempmin} degrees. Sunset at {sunset} and sunrise at {sunrise}.")
print(title)
print(desc)