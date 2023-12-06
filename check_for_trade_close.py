from libraries.binance.connect import connect_to_UMFutures
from libraries.config import MARKET, COIN_PAIR
import time
from libraries.storage.mongodb.db_TradeData import get_active_trade_ids, get_active_trade_data, delete_active_trade


def __get_active_trade_status_in_binance(client, trade_id):
    trade = client.get_all_orders(symbol=COIN_PAIR, orderId=trade_id)
    
    return trade

def __get_trade_outcome(trade_order_status, stop_loss_status, take_profit_status):
    if trade_order_status == "FILLED":
        if take_profit_status == "EXPIRED" and stop_loss_status == "NEW" or stop_loss_status == "EXPIRED" and take_profit_status == "NEW":
            return 2
        
        if stop_loss_status == "FILLED":
            return -1
        
        if take_profit_status == "FILLED":
            return 1
        
        return 0  # Trade is still open
    
    
    
def check_for_order_close(client):
    while True:
        active_trades = get_active_trade_ids()
        
        for trade_ids in active_trades:
            trade_id = trade_ids['trade_id']
            _id = trade_ids['_id']
            
            data = get_active_trade_data(trade_id)
            
             # Convert float values to integers
            trade_order_id = int(data['trade_order_id'])
            
            # Check status for trade_order_id
            trade_order_status = __get_active_trade_status_in_binance(client, str(trade_order_id))
            
            result = {}

            for order in trade_order_status:
                order_id = order['orderId']
                
                if order_id == data['trade_order_id']:
                    result['trade_order_status'] = order['status']
                
                if order_id == data['stop_loss_order_Id']:
                    result['stop_loss_order_status'] = order['status']
                
                if order_id == data['take_profit_order_id']:
                    result['take_profit_order_status'] = order['status']
            
            trade_order_status = result['trade_order_status']
            stop_loss_status = result['stop_loss_order_status']
            take_profit_status = result['take_profit_order_status']
            
            outcome = __get_trade_outcome(trade_order_status, stop_loss_status, take_profit_status)
            
            status = ""
            if outcome == 0:
                print(f"Trade: {trade_id} - Trade still open")
                status = "Active Trade"
            else:
                if outcome == 1:
                    print(f"Trade: {trade_id} - Trade closed with profit")
                    status = "Hit Take Profit"
                elif outcome == -1:
                    print(f"Trade: {trade_id} - Trade closed with loss")
                    status = "Hit Stop Loss"
                elif outcome == 2:
                    print(f"Trade: {trade_id} - Trade closed manually")
                else:
                    print("Error")
                    exit(1)
            
                delete_active_trade(_id, status)
            
        time.sleep(4)
        

        
def __select_the_market():
    if MARKET == "UMFutures":
        client = connect_to_UMFutures(use_api_keys=True)
    # elif MARKET == "Spot":
    #     client = connect_to_spot(use_api_keys=True)
    # elif MARKET == "CMFutures":
    #     client = connect_to_CMFutures(use_api_keys=True)
    else:
        print("Invalid Market")
        exit(1)
        
    return client

if __name__ == "__main__":
    client = __select_the_market()
    print("Starting... Check for Active Trades")
    
    check_for_order_close(client)
     