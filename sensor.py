# Import modules
from .data import data_generator
import pandas as pd
import requests
import json
import time
import os

# Running sensor
sensor = data_generator.SensorDataGenerator()
while True:
    sensor_data = sensor.step()
    start_time = time.time()

    sensor_data = pd.DataFrame([sensor_data])

    data = sensor_data.copy()
    data["timestamp"] = data["timestamp"].astype("str")
    data = {
        "dataframe_split": {
            "columns": data.columns.values.tolist(),
            "data": data.values.tolist()
        }
    }

    print(f"Sending:", data["dataframe_split"]["data"])

    try:
        response = requests.post(
            "http://127.0.0.1:5000/invocations",
            headers={"Content-Type": "application/json"},
         data=json.dumps(data)
        )
        print(response.json(), '\n')
    except:
        print("API not available!")
        break

    csv_path = "Anomaly-Detection/data/sensor_data.csv"
    if not os.path.exists(csv_path):
        sensor_data.to_csv(csv_path, mode='a', index=False, header=True)
    else:
        sensor_data.to_csv(csv_path, mode='a', index=False, header=False)

    elapsed = time.time() - start_time
    time.sleep(1 - elapsed)