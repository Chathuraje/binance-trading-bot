from pymongo.mongo_client import MongoClient
from libraries.config import MONGO_DB_URL, MONGO_DB_USERNAME, MONGO_DB_PASSWORD

# Constants
DB_USERNAME = MONGO_DB_USERNAME
DB_PASSWORD = MONGO_DB_PASSWORD
DB_URI = MONGO_DB_URL

client = MongoClient(f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_URI}/?retryWrites=true&w=majority")

db = client.BinanceTradingBot

trade_collection = db["trade_collection"]
active_trade_collection = db["active_trades"]