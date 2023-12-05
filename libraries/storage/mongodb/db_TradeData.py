from .models import OrderDB, ActiveTradeDB
from .connect import trade_collection, active_trade_collection


# Function to store new trade details
def create_trade(trade_data: OrderDB) -> OrderDB:

    # Insert the trade data into the MongoDB collection
    inserted_data = trade_collection.insert_one(trade_data)
    
    trade_column = {
        'trade_order_id': float(trade_data['Order ID']),
        'stop_loss_order_Id': float(trade_data['Stop Loss']['Order ID']),
        'take_profit_order_id': float(trade_data['Take Profit']['Order ID']),
        'trade_id': str(inserted_data.inserted_id)
    }
    
    active_trade_collection.insert_one(trade_column)
    return trade_data
