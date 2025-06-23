import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('./exports/traffic_data.csv')

df['is_rainy'] = (df['rain'] >= 0.1).astype(int)
df['good_weather'] = (df['temperature'] >= 4.0).astype(int)
df['busy_weekday'] = df['weekday'].apply(lambda d: 1 if d == 0 or d >= 4 else 0)
df['busy_hour'] = df['hour'].apply(lambda h: 1 if h in range(7, 10) or h in range(15, 18) else 0)

X = df[['is_rainy', 'good_weather', 'busy_weekday', 'busy_hour', 'traffic_volume', 'route_lenght']]
y = df['trip_duration_minutes']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', LinearRegression())
])

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MAE: {mae:.2f} minutes")
print(f"R² score: {r2:.2f}")

joblib.dump(pipeline, './exports/travel_time_model.pkl')
print("Model saved to ./exports/travel_time_model.pkl")