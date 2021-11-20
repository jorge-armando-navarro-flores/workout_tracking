import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import os


GENDER = "male"
WEIGHT_KG = "65"
HEIGHT_CM = 170
AGE = 23

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_new_row_endpoint = "https://api.sheety.co/36a8b23504f2db994cf6c3c9ec104cde/workoutTracking/workouts"


exercises = input("Tell me which exercises you did: ")

user_params = {
    "query": exercises,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

exercise_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

exercise_response = requests.post(exercise_endpoint, json=user_params, headers=exercise_headers)
exercises = exercise_response.json()["exercises"]

now = datetime.now()
date = now.strftime("%d/%m/%Y")
hour = now.strftime("%X")

sheet_headers = {
    "Authorization": f"Bearer {os.environ.get('TOKEN')}"
}

for exercise in exercises:
    exercise_row = {
        "date": date,
        "time": hour,
        "exercise": exercise["name"],
        "duration": exercise["duration_min"],
        "calories": exercise["nf_calories"]
    }

    new_row = {
        "workout": exercise_row
    }

    sheet_response = requests.post(sheet_new_row_endpoint, json=new_row, headers=sheet_headers)
    print(sheet_response.text)

