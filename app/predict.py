import joblib
import numpy as np

def preprocess_features(temperature, rain, weekday, hour, traffic_volume, route_length):
    is_rainy = 1 if rain >= 0.1 else 0
    good_weather = 1 if temperature >= 4.0 else 0
    busy_weekday = 1 if weekday == 0 or weekday >= 4 else 0
    busy_hour = 1 if hour in range(7, 10) or hour in range(15, 18) else 0

    return np.array([[is_rainy, good_weather, busy_weekday, busy_hour, traffic_volume, route_length]])

def predict_trip_duration(temperature, rain, weekday, hour, traffic_volume, route_length):
    model = joblib.load('../exports/travel_time_model.pkl')

    features = preprocess_features(temperature, rain, weekday, hour, traffic_volume, route_length)
    
    predicted_duration = model.predict(features)[0]
    return round(predicted_duration, 2)