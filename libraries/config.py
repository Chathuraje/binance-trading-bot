import os
from dotenv import load_dotenv
import configparser

# Load environment variables from .env file
load_dotenv()

# Access environment variables
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")


config = configparser.ConfigParser()
config.read('config.ini')

TIMEZONE = config.get('Settings', 'timezone')