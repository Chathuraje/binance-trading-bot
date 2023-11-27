import os
from dotenv import load_dotenv
import configparser

# Load environment variables from .env file
load_dotenv()

# Access environment variables
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")


# Access config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

TIMEZONE = config.get('Settings', 'timezone')
COIN_PAIR = config.get('Trading Settings', 'COIN_PAIR')
INTERVAL = config.get('Trading Settings', 'INTERVAL')
MARKET = config.get('Trading Settings', 'MARKET')
FIAT_CURRENCY = config.get('Trading Settings', 'FIAT_CURRENCY')
MINUMUM_ACCOUNT_BALANCE = config.get('Trading Settings', 'MINUMUM_ACCOUNT_BALANCE')

# Database Names
DB_NAME = config.get('Database Settings', 'DB_NAME')