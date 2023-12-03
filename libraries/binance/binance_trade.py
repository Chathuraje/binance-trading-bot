from libraries.config import MARKET, COIN_PAIR

def enter_trade(client, timestamp, latest_signal):
    
    signal_type = latest_signal['signal'].iloc[0]
    close_price = latest_signal['close'].iloc[0]
    
    quantity = latest_signal['quantity'].iloc[0]
    leverage = latest_signal['leverage'].iloc[0]
    stop_loss = latest_signal['stop_loss'].iloc[0]
    take_profit = latest_signal['take_profit'].iloc[0]
    
    if MARKET == "CMFutures" or MARKET == "UMFutures":
        # Set leverage
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

    
