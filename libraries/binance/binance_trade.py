from libraries.config import MARKET, COIN_PAIR, TIMEZONE
from libraries.storage.mongodb.db_TradeData import create_trade
from datetime import datetime
import pytz

def __save_in_db(close_price, order_data, stop_loss_data, take_profit_data):
    unix_timestamp = order_data['updateTime']
    utc_datetime = datetime.utcfromtimestamp(unix_timestamp / 1000.0)  # assuming the timestamp is in milliseconds
    target_timezone = pytz.timezone(TIMEZONE)  # replace 'Your_Target_Timezone' with the desired timezone, e.g., 'UTC', 'America/New_York', etc.
    localized_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(target_timezone)
    formatted_time = localized_datetime.strftime('%Y-%m-%d %H:%M:%S')
    
    order_columns = {
        'Order ID': order_data['orderId'],
        'Client Order ID': order_data['clientOrderId'],
        'Time': formatted_time,
        'Order Type': order_data['origType'],
        'Side': order_data['side'],
        'Position Side': order_data['positionSide'],
        'Quantity': float(order_data['origQty']),
        'Price': float(close_price),  # Include close_price as a price in order_columns
        'Stop Loss': {
            'Order ID': stop_loss_data['orderId'],
            'Client Order ID': stop_loss_data['clientOrderId'],
            'Stop Price': stop_loss_data['stopPrice']
        },
        'Take Profit': {
            'Order ID': take_profit_data['orderId'],
            'Client Order ID': take_profit_data['clientOrderId'],
            'Take Profit Price': take_profit_data['price']
        },
        'Status': "Active Trade"
    }
    

    return create_trade(order_columns)


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
        'price': take_profit,
        'timeinforce': 'GTC'
    }
        
    try:
        data = client.new_order(**params)
        print(f"Take profit order successfully placed")
        return data
        
    except Exception as e:
        print(f"Failed to place take profit order: {e}")
        exit(1)
        

def __place_the_stop_loss(client, position_side, quantity, stop_loss):
    params = {
        'symbol': COIN_PAIR,
        'side': "SELL",
        'type': 'STOP_MARKET',
        'positionSide': position_side,
        'quantity': quantity,
        'stopPrice': stop_loss,
        'timeInForce': 'GTC'
    }
        
    try:
        data = client.new_order(**params)
        print(f"Stop loss order successfully placed")
        return data
        
    except Exception as e:
        print(f"Failed to place stop loss order: {e}")
        exit(1)
        

# TODO: Make this get at the beginning
def __get_tick_size(client):
    data = client.exchange_info()
    # Assuming you want to get tick size for the first symbol
    tick_size = float(data['symbols'][0]['filters'][0]['tickSize'])
    precision = int(data['symbols'][0]['filters'][0]['tickSize'].split('.')[1].find('1'))
    
    return tick_size, precision

    
    
def __adjust_to_tick_size(price, tick_size, precision):
    # Calculate adjusted price based on tick size and precision
    adjusted_price = round(price / tick_size) * tick_size
    
    return round(adjusted_price, precision)



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
        
    tick_size, precision = __get_tick_size(client)
    
    adjusted_take_profit = __adjust_to_tick_size(take_profit, tick_size, precision)
    adjusted_stop_loss = __adjust_to_tick_size(stop_loss, tick_size, precision)
    
    order_data = __place_the_order(client, position_side, quantity)  
    take_profit_data = __place_the_take_profit(client, position_side, order_data['origQty'], adjusted_take_profit)
    stop_loss_data = __place_the_stop_loss(client, position_side, order_data['origQty'], adjusted_stop_loss)
    
    __save_in_db(close_price, order_data, stop_loss_data, take_profit_data)