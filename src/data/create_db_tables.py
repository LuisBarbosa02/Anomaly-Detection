# Import libraries
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import BigInteger, Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy import create_engine
from ..config import SENSOR_DATABASE_URL

# Define tables
Base = declarative_base()
class SensorData(Base):
    """
    Definition of table to store the raw sensor data.
    """
    # Table name
    __tablename__ = "sensor_data"

    # Defining columns
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    sound = Column(Float, nullable=False)
    anomaly = Column(Integer, nullable=False)

    predictions = relationship("Predictions", back_populates="sensordata",
                               uselist=False, cascade="all, delete-orphan", passive_deletes=True)

class Predictions(Base):
    """
    Definition of table to store predictions.
    """
    # Table name
    __tablename__ = "predictions"

    # Defining columns
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    sensor_data_id = Column(BigInteger, ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False, unique=True)
    prediction = Column(Integer, nullable=False)

    sensordata = relationship("SensorData", back_populates="predictions")

# Create tables
if __name__ == "__main__":
    # Create engine for PostgreSQL database connection
    engine = create_engine(SENSOR_DATABASE_URL)

    # Create tables automatically at startup
    Base.metadata.create_all(engine)