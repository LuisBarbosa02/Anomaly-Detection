# Import libraries
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import BigInteger, Column, Integer, DateTime, Float, ForeignKey, text

# Define table
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

# Define function and trigger for tables
def create_limited_table(database):
    """
    Function to create a function and a trigger in PostgreSQL to limit tables to 50000 samples.
    """
    with database.connect() as connection:
        # Create function
        connection.execute(text("""
        CREATE OR REPLACE FUNCTION enforce_sensor_data_limit()
        RETURNS TRIGGER AS $$
        BEGIN
            DELETE FROM sensor_data
            WHERE id IN (
                SELECT id
                FROM sensor_data
                ORDER BY timestamp DESC
                OFFSET 50000
            );
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """))

        # Drop trigger if exists
        connection.execute(text("""
        DROP TRIGGER IF EXISTS sensor_data_limit_trigger
        ON sensor_data;
        """))

        # Create trigger
        connection.execute(text("""
        CREATE TRIGGER sensor_data_limit_trigger
        AFTER INSERT ON sensor_data
        FOR EACH ROW
        EXECUTE FUNCTION enforce_sensor_data_limit();
        """))
    
        # Commit changes
        connection.commit()