import os
from dotenv import load_dotenv
import configparser

# Access config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

MODE = config.get('Settings', 'MODE')

TIMEZONE = config.get('Settings', 'timezone')
COIN_PAIR = config.get('Trading Settings', 'COIN_PAIR')
INTERVAL = config.get('Trading Settings', 'INTERVAL')
MARKET = config.get('Trading Settings', 'MARKET')
FIAT_CURRENCY = config.get('Trading Settings', 'FIAT_CURRENCY')
MINUMUM_ACCOUNT_BALANCE = config.get('Trading Settings', 'MINUMUM_ACCOUNT_BALANCE')
RISK_AMOUNT = config.get('Trading Settings', 'RISK_AMOUNT')
MAX_ORDERS = config.get('Trading Settings', 'MAX_ORDERS')

# Database Names
DB_NAME = config.get('Database Settings', 'DB_NAME')



# Load environment variables from .env file
load_dotenv()

# Access environment variables

if MODE == 'TESTNET':
    if MARKET == 'UMFutures' or MARKET == 'CMFutures':
        BINANCE_API_KEY = os.getenv("BINANCE_API_KEY_TESTNET_FUTURE")
        BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY_TESTNET_FUTURE")
    elif MARKET == 'Spot':
        BINANCE_API_KEY = os.getenv("BINANCE_API_KEY_TESTNET_SPOT")
        BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY_TESTNET_SPOT")
    
    MONGO_DB_URL = os.getenv("MONGO_DB_URL_TEST")
    MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME_TEST")
    MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD_TEST")
    
elif MODE == 'LIVE':
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
    MONGO_DB_URL = os.getenv("MONGO_DB_URL")
    MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
    MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
else:
    print("Invalid Mode. Please set MODE to either 'TESTNET' or 'LIVE'")
    exit(1)