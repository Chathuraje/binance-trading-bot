from .models import OrderDB
from .connect import trade_collection

# Function to store new trade details
def create_trade(trade_data: OrderDB) -> OrderDB:

    # Insert the trade data into the MongoDB collection
    trade_collection.insert_one(trade_data)
    
    return trade_data
