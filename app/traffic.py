from dotenv import load_dotenv
from typing import Tuple, List
import requests
import os

load_dotenv()

def get_route_length(start_cords: Tuple, end_cords: Tuple) -> float:
    latitude1, longitude1 = start_cords
    latitude2, longitude2 = end_cords

    url = f'https://api.tomtom.com/routing/1/calculateRoute/{latitude1},{longitude1}:{latitude2},{longitude2}/json?traffic=false&key={os.getenv('TOMTOM_API_KEY')}'
    
    try:
        data = requests.get(url).json()

        route_length = data['routes'][0]['summary']['lengthInMeters'] / 1000
        return route_length
    except Exception as e:
        print(f"[ERROR] Error while retrieving route: {e}")
        return None
