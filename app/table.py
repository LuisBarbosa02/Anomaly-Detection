# Import libraries
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import BigInteger, Column, Integer, ForeignKey

# Define table
Base = declarative_base()
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