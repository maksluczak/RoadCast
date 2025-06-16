from dotenv import load_dotenv
import requests
import os

load_dotenv()

def get_coordinates_from_address(address: str):
    url = 'https://geocode.maps.co/search'
    resp = requests.get(url, params={'q': address, 'api_key': os.getenv('GEOCODE_API_KEY')})
    data = resp.json()
    
    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    else:
        return None, None