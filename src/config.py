# Import libraries
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATA_FOLDER = os.environ['DATA_FOLDER']
DATA_PATH = os.environ['DATA_PATH']
PREPROCESSOR_PATH = os.environ['PREPROCESSOR_PATH']
MODEL_PATH = os.environ['MODEL_PATH']
PIPELINE_PATH = os.environ['PIPELINE_PATH']
SENSOR_DATABASE_URL = os.environ['SENSOR_DATABASE_URL']
SENSOR_DATA_PATH = os.environ['SENSOR_DATA_PATH']