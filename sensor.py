# Import modules
from src.data.data_generator import SensorDataGenerator
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
	
	while True:
		# Get one sensor step
		sensor_data = sensor.step()
		
		# Start time
		start_time = time.time()

		# Make prediction request to served model
		try:
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