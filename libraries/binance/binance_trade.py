from libraries.config import MARKET, COIN_PAIR


def __save_in_db(data):
    print(data)

def __place_the_order(client, position_side, quantity):
    
    params = {
        'symbol': COIN_PAIR,
        'side': "BUY",
        'type': 'MARKET',
        'positionSide': position_side,
        'quantity': quantity,
    }
        
    try:
        data = client.new_order(**params)
        # client.new_order_test(**params)
        print(f"Order successfully placed")

        __save_in_db(data)
        
        return data
        
    except Exception as e:
        print(f"Failed to place order: {e}")
        exit(1)
       
       
def __place_the_take_profit(client, position_side, quantity, take_profit):
    params = {
        'symbol': COIN_PAIR,
        'side': "SELL",
        'type': 'LIMIT',
        'positionSide': position_side,
        'quantity': quantity,
        'price': '40000.2',
        'timeinforce': 'GTC'
    }
        
    try:
        data = client.new_order(**params)
        # client.new_order_test(**params)
        print(f"Order successfully placed")

        __save_in_db(data)
        
        return data
        
    except Exception as e:
        print(f"Failed to place order: {e}")
        exit(1)      
        

def __place_the_stop_loss(client, position_side, quantity, stop_loss):
    params = {
        'symbol': COIN_PAIR,
        'side': "SELL",
        'type': 'STOP_MARKET',
        'positionSide': position_side,
        'quantity': quantity,
        'stopPrice': '35000.2',
        'timeinforce': 'GTC'
    }
        
    try:
        data = client.new_order(**params)
        # client.new_order_test(**params)
        print(f"Order successfully placed")

        __save_in_db(data)
        
        return data
        
    except Exception as e:
        print(f"Failed to place order: {e}")
        exit(1)
        

def enter_trade(client, timestamp, latest_signal):
    signal_type = latest_signal['signal'].iloc[0]
    close_price = latest_signal['close'].iloc[0]
    
    quantity = latest_signal['quantity'].iloc[0]
    leverage = latest_signal['leverage'].iloc[0]
    stop_loss = latest_signal['stop_loss'].iloc[0]
    take_profit = latest_signal['take_profit'].iloc[0]
    
    print(f"New Signal Received - Timestamp: {timestamp}, Signal Type: {signal_type} ({'Buy' if signal_type == 1 else 'Sell'}), Close Price: {close_price}, Leverage: {leverage}, Quantity: {quantity}, Take Loss: {stop_loss}, Take Profit: {take_profit}")
    
    if MARKET == "CMFutures" or MARKET == "UMFutures":
        # Set leverage
        client.change_leverage(symbol=COIN_PAIR, leverage=leverage)
        
    if signal_type == 1:
        position_side = "LONG"
    elif signal_type == -1:
        position_side = "SHORT"
    else:
        print("Invalid signal_type")
        exit(1)
    
    __place_the_order(client, position_side, quantity)  
    __place_the_stop_loss(client, position_side, quantity, stop_loss)
    __place_the_take_profit(client, position_side, quantity, take_profit)
    

    
    
    
    
