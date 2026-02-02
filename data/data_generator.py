# Import libraries
import numpy as np
import pandas as pd
from datetime import timedelta

# Default values
class SensorState:
    temperature = 22.0
    humidity = 45.0
    sound = 68.0

# Anomaly injection
class AnomalyInjector:
    def __init__(self, anomaly_probability=0.001):
        self.anomaly_probability = anomaly_probability
        self.active_fault = None
        self.remaining_steps = 0

    # Randomly start an anomaly
    def start_fault(self):
        if self.active_fault is None and np.random.rand() < self.anomaly_probability:
            self.active_fault = np.random.choice(
                ['overheating', 'mechanical', 'environmental']
            )
            self.remaining_steps = np.random.randint(30, 120)

    # Apply the anomaly to the sensor's state
    def apply_fault(self, state):
        if self.active_fault is None:
            return state, 1

        if self.active_fault == 'overheating':
            state.temperature += np.random.normal(0.4, 0.1)
            state.sound += np.random.normal(1.0, 0.4)

        elif self.active_fault == 'mechanical':
            state.sound += np.random.normal(2.5, 0.8)

        elif self.active_fault == 'environmental':
            state.humidity += np.random.normal(0.6, 0.15)

        self.remaining_steps -= 1
        if self.remaining_steps <= 0:
            self.active_fault = None

        return state, -1

# Data generator
class SensorDataGenerator:
    def __init__(self):
        self.state = SensorState()
        self.anomaly_injector = AnomalyInjector()
        self.current_time = pd.to_datetime('now').round(freq='s')

        self.params = {
            "temperature": {"mu": 22.0, "theta": 0.05, "sigma": 0.05},
            "humidity": {"mu": 45.0, "theta": 0.04, "sigma": 0.10},
            "sound": {"mu": 68.0, "theta": 0.03, "sigma": 0.30},
        }

    def mean_reverting_step(self, x, mu, theta, sigma):
        return x + theta * (mu - x) + np.random.normal(0, sigma)

    # Data generator step
    def step(self):
        p = self.params
        s = self.state

        s.temperature = self.mean_reverting_step(
            s.temperature, p["temperature"]["mu"],
            p["temperature"]["theta"], p["temperature"]["sigma"]
        )

        s.humidity = self.mean_reverting_step(
            s.humidity, p["humidity"]["mu"],
            p["humidity"]["theta"], p["humidity"]["sigma"]
        )

        s.sound = self.mean_reverting_step(
            s.sound, p["sound"]["mu"],
            p["sound"]["theta"], p["sound"]["sigma"]
        )

        # Possible anomaly
        self.anomaly_injector.start_fault()
        self.state, anomaly = self.anomaly_injector.apply_fault(self.state)

        # Time logic
        timestamp = self.current_time
        self.current_time += timedelta(seconds=1)

        return {
            "timestamp": timestamp,
            "temperature": round(self.state.temperature, 2),
            "humidity": round(self.state.humidity, 2),
            "sound": round(self.state.sound, 2),
            "anomaly": anomaly
        }