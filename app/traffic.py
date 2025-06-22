from dotenv import load_dotenv
from typing import Tuple, List, Optional
import requests
import os

load_dotenv()

def get_route_length(start_cords: Tuple, end_cords: Tuple) -> Optional[float]:
    latitude1, longitude1 = start_cords
    latitude2, longitude2 = end_cords

    url = f"https://api.tomtom.com/routing/1/calculateRoute/{latitude1},{longitude1}:{latitude2},{longitude2}/json?traffic=false&key={os.getenv('TOMTOM_API_KEY')}"
    
    try:
        data = requests.get(url).json()

        route_length = data['routes'][0]['summary']['lengthInMeters'] / 1000
        return route_length
    except Exception as e:
        print(f"[ERROR] Error while retrieving route: {e}")
        return None
    
def get_traffic_volume(start_cords: Tuple, end_cords: Tuple) -> Optional[float]:
    points = generate_route_points(start_cords, end_cords, 5)
    traffic_volume = []

    for lat, lon in points:
        url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&unit=KMPH&key={os.getenv('TOMTOM_API_KEY')}"

        try:
            resp = requests.get(url)
            resp.raise_for_status()
            data = resp.json()

            segment = data.get('flowSegmentData', {})
            currentSpeed = segment.get('currentSpeed')
            freeFlowSpeed = segment.get('freeFlowSpeed')

            if currentSpeed and freeFlowSpeed:
                vol = 1 - (currentSpeed / freeFlowSpeed)
                traffic_volume.append(vol)
        except Exception as e:
            print(f"[ERROR] Error while retrieving route: {e}")
        
    if traffic_volume:
        return sum(traffic_volume) / len(traffic_volume)
    else:
        return None

def generate_route_points(start_cords: Tuple, end_cords: Tuple, n: int) -> List[Tuple[float]]:
    latitude1, longitude1 = start_cords
    latitude2, longitude2 = end_cords

    return [
        (
            latitude1 + (latitude2 - latitude1) * i / (n - 1),
            longitude1 + (longitude2 - longitude1) * i / (n - 1)
        )
        for i in range(n)
    ]