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


def get_active_trade_count():
    return int(active_trade_collection.count_documents({}))


def get_active_trade_ids():
    # Fetch active trades from the collection
    active_trades = active_trade_collection.find({}, {'_id': 1, 'trade_id': 1})

    # Extract trade_id and _id from each trade
    trade_ids = [{'trade_id': trade['trade_id'], '_id': trade['_id']} for trade in active_trades]

    return trade_ids

# get active trade data using trade_id
def get_active_trade_data(trade_id: str) -> OrderDB:
    trade_data = active_trade_collection.find_one({'trade_id': trade_id}, {'_id': 0, 'trade_id': 0})
    
    return trade_data


# def __update_trade_status(trade_id: str, status: str):
#     # Update the trade status in the collection
#     if trade_id is not None:
#         # Update the trade status in the collection
#         trade_collection.update_one({'_id': trade_id}, {'$set': {'status': status}})
#     else:
#         print(f"Invalid trade_id: {trade_id}")
    

def delete_active_trade(trade_id, status):
    
    trade_id = active_trade_collection.find_one({'trade_id': trade_id}, {'_id': 0, 'trade_id': 0})
    result = active_trade_collection.delete_one({"_id": trade_id})

    # Check if the deletion was successful
    if result.deleted_count == 1:
         # Get tradeID from active_trade_collection
        
        print(trade_id)
        # __update_trade_status(trade_id, status)
    else:
        print(f"No document found with _id {trade_id}.")
    
