from dotenv import load_dotenv
import requests
import os

load_dotenv()

def get_current_weather_by_city(city: str):
    url = f'http://api.openweathermap.org/data/2.5/weather?appid={os.getenv("WEATHER_API_KEY")}&q={city}&units=metric'
    try:
        data = requests.get(url).json()

        return {
            'temperature': data['main']['temp'],
            'rain': data.get('rain', {}).get('1h', 0.0)
        }
    except Exception as e:
        print(f"[ERROR] Error while retrieving weather: {e}")
        return None