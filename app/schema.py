# Import libraries
from pydantic import BaseModel

# Data schema
class Features(BaseModel):
    """
    Schema for Features to be used.
    """
    timestamp: str
    temperature: float
    humidity: float
    sound: float
    anomaly: int