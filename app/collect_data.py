from weather import get_current_weather_by_city
from traffic import get_route_length, get_traffic_volume
from utils import get_datetime, get_coordinates_from_address
from database import insert_data
import datetime

city = "Warsaw"
start = get_coordinates_from_address('Aleje Jerozolimskie 1, ' + city)
end = get_coordinates_from_address('Plac Grzybowski 10, ' + city)
trip_duration_minutes = 12

if not start or not end:
    print("[ERROR] Failed to retrieve coordinates.")
    exit()

weekday, hour = get_datetime(datetime.datetime.now())
weather = get_current_weather_by_city(city)

if not weather:
    print("[ERROR] Failed to retrieve weather data.")
    exit()

traffic_volume = get_traffic_volume(start, end)
route_length = get_route_length(start, end)

if None in [traffic_volume, route_length]:
    print("[ERROR] Missing traffic or route length data.")
    exit()

insert_data(
    weekday=weekday,
    hour=hour,
    temperature=weather['temperature'],
    rain=weather['rain'],
    traffic_volume=traffic_volume,
    route_length=route_length,
    trip_duration_minutes=trip_duration_minutes
)
