from dotenv import load_dotenv
import datetime
import requests
import os

load_dotenv()

def get_datetime(date: datetime):
    return date.weekday(), date.hour

def get_coordinates_from_address(address: str):
    url = 'https://geocode.maps.co/search'
    try:
        resp = requests.get(url, params={'q': address, 'api_key': os.getenv('GEOCODE_API_KEY')})
        resp.raise_for_status()

        data = resp.json()

        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
        else:
            print(f"[ERROR] No data found for address: {address}")
            return None, None

    except Exception as e:
        print(f"[ERROR] Failed to retrieve coordinates for '{address}': {e}")
        return None, None
