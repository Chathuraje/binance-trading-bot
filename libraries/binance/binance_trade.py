from libraries.config import MARKET, COIN_PAIR
from binance.spot import Spot
from binance.cm_futures import CMFutures
from binance.um_futures import UMFutures

def enter_trade(client, timestamp, latest_signal):
    
    signal_type = latest_signal['signal'].iloc[0]
    close_price = latest_signal['close'].iloc[0]
    
    quantity = latest_signal['quantity'].iloc[0]
    leverage = latest_signal['leverage'].iloc[0]
    stop_loss = latest_signal['stop_loss'].iloc[0]
    take_profit = latest_signal['take_profit'].iloc[0]
    
    if MARKET == "CMFutures" or MARKET == "UMFutures":
        try:
            client.change_position_mode(dualSidePosition=True) # change position mode to Hedge Mode
        except:
            print(f"Failed to change position mode to Hedge Mode or current position mode is already Hedge Mode")
        
        try:
            client.change_margin_type(symbol=COIN_PAIR, marginType='CROSSED')
        except:
            print(f"Failed to change margin type to CROSSED or current margin type is already CROSSED")
        
        client.change_leverage(symbol=COIN_PAIR, leverage=leverage)
    
    if signal_type == 1:
        side = "BUY"
        positionSide = "LONG"
    elif signal_type == -1:
        side = "SELL"
        positionSide = "SHORT"
    else:
        print("Invalid signal_type")
        
    params = {
        'symbol': COIN_PAIR,
        'side': side,
        'type': 'MARKET',
        'positionSide': positionSide,
        'quantity': quantity,
    }
        
    try:
        #client.new_order(**params)
        client.new_order_test(**params)
        print (f"timestamp: {timestamp}, signal_type: {signal_type}, close_price: {close_price}")
        
    except Exception as e:
        print(f"Failed to place order: {e}")
        return False

    
