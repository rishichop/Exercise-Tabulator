import datetime
import os
import requests

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
SHEETY_USERNAME = os.environ.get("SHEETY_USERNAME")
SHEETY_PROJECT_NAME = os.environ.get("SHEETY_PROJECT_NAME")
SHEETY_SHEET_NAME = os.environ.get("SHEETY_SHEET_NAME")
SHEETY_AUTH = os.environ.get("SHEETY_AUTH")

API_HEADER_NUTRITION = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

API_HEADER_SHEETY = {
    "Authorization": SHEETY_AUTH
}

EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = f"https://api.sheety.co/{SHEETY_USERNAME}/{SHEETY_PROJECT_NAME}/{SHEETY_SHEET_NAME}"

today_exercise = input("Enter how much Exercise did you do: ")

exercise_params = {
    "query": today_exercise,
    "gender": "male",
    "weight_kg": 70,
    "height_cm": 165,
    "age": 20
}

today = datetime.datetime.now()
time = today.strftime("%I:%M:%S%p")
date = today.strftime("%d/%m/%Y")

response = requests.post(url=EXERCISE_ENDPOINT, json=exercise_params, headers=API_HEADER_NUTRITION)

for exercise in response.json()["exercises"]:
    exercise_name = exercise["name"].title()
    duration = exercise["duration_min"]
    calories = exercise["nf_calories"]

    sheety_params = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise_name,
            "duration": duration,
            "calories": calories
        }
    }
    print(sheety_params)

    sheety_response = requests.post(url=SHEETY_ENDPOINT, json=sheety_params, headers=API_HEADER_SHEETY)
    print(sheety_response.json())
