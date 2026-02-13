# Import libraries
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

PIPELINE_PATH = os.environ['PIPELINE_PATH']
DATABASE_URL = os.environ['DATABASE_URL']