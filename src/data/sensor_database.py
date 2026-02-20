# Import libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import SENSOR_DATABASE_URL

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