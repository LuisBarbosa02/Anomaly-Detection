# Import libraries
from .table import Base
from .database import engine, get_db, save_prediction
from fastapi import FastAPI, Depends
import pickle
from .config import PIPELINE_PATH
from .schema import Features
from sqlalchemy.orm import Session
import pandas as pd

# Create table automatically at startup
Base.metadata.create_all(bind=engine)

# Create application
app = FastAPI()

# Load pipeline
with open(PIPELINE_PATH, 'rb') as file:
    pipeline = pickle.load(file)

# App home
@app.get("/")
def home():
    """
    Web page home.
    """
    return {"welcome": "Wind turbine anomaly detection model",
            "instruction": "Use the extension '/predict' to make a prediction"}

# App status
@app.get("/status")
def status():
    """
    Web page status.
    """
    return {"status": "Model is up and running!"}

# App prediction
@app.post("/predict")
def predict(features: Features, db: Session = Depends(get_db)):
    """
    Make a prediction from the served model.
    """
    # Arrange data
    input_data = pd.DataFrame([features.dict()])

    # Make prediction
    prediction = int(pipeline.predict(input_data)[0])

    # Save prediction
    save_prediction(db, prediction)

	# Result
    result = features.dict()
    result['prediction'] = prediction

    return result