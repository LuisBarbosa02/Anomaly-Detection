# Import libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import SENSOR_DATABASE_URL
from .create_db_tables import SensorData

# Create engine for postgresql database connection
sensor_engine = create_engine(SENSOR_DATABASE_URL)

# Create session referencing the engine
SensorSessionLocal = sessionmaker(bind=sensor_engine)

# Create a session to the database
def get_sensor_db():
    """
    Connect to database.
    :return:
    """
    return SensorSessionLocal()

# Saving to database
def save_sensor_database(db, sensor_data):
    """
    Function to save raw data to database
    """
    # Save values into table
    raw_data = SensorData(
            timestamp=sensor_data['timestamp'],
            temperature=sensor_data['temperature'],
            humidity=sensor_data['humidity'],
            sound=sensor_data['sound'],
            anomaly=sensor_data['anomaly']
        )

    # Add prediction to database
    db.add(raw_data)

    # Commit change
    db.commit()

    # Refresh
    db.refresh(raw_data)

    # Close connection with database
    db.close()