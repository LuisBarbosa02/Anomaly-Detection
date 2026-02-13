# Import libraries
from sqlalchemy import create_engine
from .config import DATABASE_URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from .table import Predictions

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
def save_prediction(db: Session, prediction: int):
    """
    Save a single prediction to PostgreSQL database.
    """
    # Prediction
    prediction = Predictions(
        prediction=prediction
    )

    # Add prediction to database
    db.add(prediction)

    # Commit change
    db.commit()

    # Refresh
    db.refresh(prediction)