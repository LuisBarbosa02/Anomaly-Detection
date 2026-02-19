# Import libraries
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, BigInteger, DateTime, Float, Integer

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