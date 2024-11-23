import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the project root directory (parent of fine_tuning)
ROOT_DIR = Path(__file__).parent.parent
ENV_FILE = ROOT_DIR / '.env'

logger.info(f"Looking for .env file at: {ENV_FILE}")
logger.info(f"File exists: {ENV_FILE.exists()}")

# Try to find .env file automatically
dotenv_path = find_dotenv()
logger.info(f"Dotenv path found: {dotenv_path}")

# Load environment variables from .env file in project root
success = load_dotenv(ENV_FILE)
logger.info(f"Load_dotenv success: {success}")

# Log environment variable status
GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
logger.info(f"API Key loaded: {'Yes' if GEMINI_API_KEY else 'No'}")

# API Keys and URLs
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# API Settings
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30

# Query Settings
MAX_QUERY_LENGTH = 1000
CACHE_TIMEOUT = 3600  # 1 hour 

# Fine-tuning Settings
FINE_TUNED_MODEL_NAME = os.getenv('FINE_TUNED_MODEL_NAME', 'gemini-flash')
TRAINING_DATA_DIR = "fine_tuning/training_data"

# Model Validation Settings
MIN_SUCCESS_RATE = 0.95
MIN_SQL_VALIDITY_RATE = 0.98
MAX_RESPONSE_TIME = 2.0  # seconds