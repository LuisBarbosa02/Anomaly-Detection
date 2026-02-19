# Import libraries
from sqlalchemy import create_engine
from .config import DATABASE_URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from .table import SensorData, Predictions

# Create engine for postgresql database connection
engine = create_engine(DATABASE_URL)

# Create session referencing the engine
SessionLocal = sessionmaker(bind=engine)

# Create a session to the database
def get_db():
    """
    Connect to database.
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Save to database
def save_sensor_data(db: Session, data: SensorData):
    """
    Save single raw sensor data into PostgreSQL database.
    """
    # Save sensor data into table
    sensor_data = SensorData(
        timestamp=data.timestamp,
        temperature=data.temperature,
        humidity=data.humidity,
        sound=data.sound,
        anomaly=data.anomaly
    )

    # Add prediction to database
    db.add(sensor_data)

    # Flush change
    db.flush() # Send changes to current database session, but do not commit it to subsequent sessions

    return sensor_data

def save_prediction(db: Session, sensor_id: int, prediction: int):
    """
    Save a single prediction to PostgreSQL database.
    """
    # Prediction
    prediction = Predictions(
        sensor_data_id=sensor_id,
        prediction=prediction
    )

    # Add prediction to database
    db.add(prediction)

    # Commit change
    db.commit()

    # Refresh
    db.refresh(prediction)