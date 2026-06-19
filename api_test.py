import os
import requests

from dotenv import load_dotenv

load_dotenv()

OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")


def get_coordinates(city):

    url = "https://api.opencagedata.com/geocode/v1/json"

    params = {
        "q": city,
        "key": OPENCAGE_API_KEY,
        "limit": 1
    }

    response = requests.get(url, params=params)

    print("Status:", response.status_code)
    print(response.text)

    data = response.json()

    if data["results"]:

        geometry = data["results"][0]["geometry"]

        return (
            geometry["lat"],
            geometry["lng"]
        )

    return None


city = "Barcelona"

coordinates = get_coordinates(city)

print(f"City: {city}")
print(f"Coordinates: {coordinates}")