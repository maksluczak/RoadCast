from dotenv import load_dotenv
import requests
import os

load_dotenv()

def get_current_weather_by_city(city='Cracow'):
    url = f'http://api.openweathermap.org/data/2.5/weather?appid={os.getenv("WEATHER_API_KEY")}&q={city}&units=imperial'
    data = requests.get(url).json()
    
    return {
        'temperature': data['main']['temp'],
        'rain': data.get('rain', {}).get('1h', 0.0)
    }