from flask import Blueprint, render_template, request, redirect, url_for, flash
from .weather import get_current_weather_by_city
from .traffic import get_route_length, get_traffic_volume
from .utils import get_datetime, get_coordinates_from_address
from .predict import predict_trip_duration
from .database import insert_data
import joblib
import datetime

main = Blueprint('main', __name__)

model = joblib.load('../exports/travel_time_model.pkl')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/predict', methods=['POST'])
def predict():
    try:
        start_address = request.form['start'].strip()
        end_address = request.form['end'].strip()
        city = request.form['city'].strip()

        weekday, hour = get_datetime(datetime.datetime.now())
        
        weather = get_current_weather_by_city(city)
        temperature=weather['temperature']
        rain=weather['rain']

        start = get_coordinates_from_address(start_address + ', ' + city)
        end = get_coordinates_from_address(end_address + ', ' + city)

        traffic_volume = get_traffic_volume(start, end)
        route_length = get_route_length(start, end)

        prediction = predict_trip_duration(temperature, rain, weekday, hour, traffic_volume, route_length)

        insert_data(
            weekday=weekday,
            hour=hour,
            temperature=temperature,
            rain=rain,
            traffic_volume=traffic_volume,
            route_length=route_length,
            trip_duration_minutes=prediction
        )

        return render_template('predict.html', 
                               duration=prediction, 
                               start=start_address,
                               end=end_address,
                               city=city,
                               route_length=round(route_length, 2),
                               traffic=round(traffic_volume * 100, 1),
                               rain_mm=rain,
                               temp=temperature)

    except Exception as e:
        flash(f"[ERROR] Failed to retrieve data: {e}")
        return redirect(url_for('main.index'))