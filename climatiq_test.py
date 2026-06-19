import os
import requests

from dotenv import load_dotenv

load_dotenv()

CLIMATIQ_API_KEY = os.getenv("CLIMATIQ_API_KEY")

url = "https://preview.api.climatiq.io/travel/v1-preview3/distance"

headers = {
    "Authorization": f"Bearer {CLIMATIQ_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "travel_mode": "rail",
    "origin": {
        "query": "Berlin"
    },
    "destination": {
        "query": "Barcelona"
    }
}

response = requests.post(
    url,
    json=payload,
    headers=headers
)

print("Status Code:", response.status_code)
print()
print(response.text)