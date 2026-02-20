# Import libraries
from ..config import DATA_PATH, SENSOR_DATA_PATH
import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset
import sys

# Check drift
def check_dataset_drift(threshold=0.5):
    """
    Check if the dataset has drifted.
    :return: Boolean
    """
    # Load data
    reference_data = pd.read_csv(DATA_PATH).drop(columns=['timestamp', 'anomaly']) # Training data

    new_data = pd.read_csv(SENSOR_DATA_PATH, index_col='id').drop(columns=['timestamp', 'anomaly']) # Sensor data

    # Drift report
    report = Report([
        DataDriftPreset()
    ])
    report = report.run(reference_data=reference_data, current_data=new_data)
    
    # Get the report's dictionary
    report_dict = report.dict()

    # Localize the amount of drift in the dataset
    drift_metric = next(m for m in report_dict['metrics'] if 'DriftedColumnsCount' in m['metric_name'])
    drift_share = drift_metric['value']['share']

    if drift_share >= threshold:
        return True # Drift detected
    return False # No drift

# Run detection
if __name__ == '__main__':
    drift_detected = check_dataset_drift()

    if drift_detected:
        print("❌ DATA DRIFT DETECTED")
        sys.exit(1)
    else:
        print("✅ NO DRIFT")
        sys.exit(0)