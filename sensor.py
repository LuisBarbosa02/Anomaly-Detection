# Import modules
from src.data.data_generator import SensorDataGenerator
from src.data.sensor_database import get_sensor_db, save_sensor_database
import signal
import time
import requests

# Sensor
def run_sensor():
    """
    Function to run the simulated sensor.
    """
    # Handle KeyboardInterrupt shutdown
    running = True
    def handle_keyboardinterrupt(signum, frame):
        nonlocal running
        print("\nShutdown signal received. Finishing current cycle...")
        running = False
    signal.signal(signal.SIGINT, handle_keyboardinterrupt)

    # Sensor
    sensor = SensorDataGenerator()

    # Sensor logic
    with get_sensor_db() as sensor_db: # Create engine and session with the sensor database
        while running:
            # Get one sensor step
            sensor_data = sensor.step()

            # Start time
            start_time = time.time()

            # Save raw sensor data to database
            save_sensor_database(sensor_db, sensor_data)

            # Make prediction request to served model
            try:
                request_data = sensor_data.copy()
                request_data['timestamp'] = str(request_data['timestamp']) # Request do not accept Timestamp format
                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    headers={"Content-Type": "application/json"},
                    json=request_data,
                    timeout=5
               )

                if response.status_code == 200:
                    print(response.json(), '\n')

                else:
                    print("Prediction failed:", response.status_code)
                    print("Response text:", response.text)
            
            except Exception as e:
                print("API not available:", e)

            # Elapsed time
            elapsed = time.time() - start_time

            # Wait 1 second from start time
            sleep_time = max(0, 1 - elapsed) # Avoid break if more than 1 second
            if running:
                time.sleep(sleep_time)

# Run sensor
if __name__ == '__main__':
    run_sensor()