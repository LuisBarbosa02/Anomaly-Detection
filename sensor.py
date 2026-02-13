# Import modules
from src.data.data_generator import SensorDataGenerator
from sqlalchemy import create_engine
from src.data.sensor_database import sensor_engine, get_sensor_db, save_sensor_database
from src.data.create_db_tables import Base, SensorData
import pandas as pd
import time
import requests
import os

# Sensor
def run_sensor():
    """
    Function to run the simulated sensor.
    """
    # Sensor
    sensor = SensorDataGenerator()

    # Generate tables automatically at startup
    Base.metadata.create_all(bind=sensor_engine)

    while True:
        # Get one sensor step
        sensor_data = sensor.step()

        # Start time
        start_time = time.time()

        # Create engine and session with the sensor database
        sensor_db = get_sensor_db()

        # Save raw sensor data to database
        save_sensor_database(sensor_db, sensor_data)

        # Make prediction request to served model
        try:
            sensor_data['timestamp'] = str(sensor_data['timestamp']) # Request do not accept Timestamp format
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                headers={"Content-Type": "application/json"},
                json=sensor_data
            ).json()
            print(response, '\n')
        except:
            print("API not available!")
            break

        # Save prediction
        csv_path = "data/sensor_data.csv"
        df = pd.DataFrame([response])
        if not os.path.exists(csv_path):
            df.to_csv(csv_path, mode='a', index=False, header=True)
        else:
            df.to_csv(csv_path, mode='a', index=False, header=False)

        # Elapsed time
        elapsed = time.time() - start_time

        # Wait 1 second from start time
        time.sleep(1 - elapsed)

# Run sensor
if __name__ == '__main__':
    run_sensor()