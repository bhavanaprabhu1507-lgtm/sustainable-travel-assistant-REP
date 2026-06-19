import os
import requests

from dotenv import load_dotenv

load_dotenv()

OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")
OPENROUTESERVICE_API_KEY = os.getenv(
    "OPENROUTESERVICE_API_KEY"
)


def get_coordinates(city):

    url = "https://api.opencagedata.com/geocode/v1/json"

    params = {
        "q": city,
        "key": OPENCAGE_API_KEY,
        "limit": 1
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    geometry = data["results"][0]["geometry"]

    return (
        geometry["lng"],
        geometry["lat"]
    )


def get_distance(origin, destination):

    start = get_coordinates(origin)
    end = get_coordinates(destination)

    url = (
        "https://api.openrouteservice.org/v2/directions/driving-car"
    )

    headers = {
        "Authorization": OPENROUTESERVICE_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            start,
            end
        ]
    }

    response = requests.post(
        url,
        json=body,
        headers=headers
    )

    print("\nStatus Code:", response.status_code)
    print("\nResponse:")
    print(response.text)

    data = response.json()

    if "routes" not in data:
        return None

    distance_meters = (
        data["routes"][0]["summary"]["distance"]
    )

    distance_km = round(
        distance_meters / 1000,
        2
    )

    return distance_km


origin = "Berlin"
destination = "Barcelona"

distance = get_distance(
    origin,
    destination
)

print("\nOrigin:", origin)
print("Destination:", destination)
print("Distance:", distance)

print("OpenCage Loaded:", OPENCAGE_API_KEY is not None)
print("OpenRoute Loaded:", OPENROUTESERVICE_API_KEY is not None)