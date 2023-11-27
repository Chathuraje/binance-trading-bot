from libraries.binance.connect import connect_to_UMFutures
from libraries.config import TIMEZONE, COIN_PAIR, INTERVAL
import json
import websocket
import pandas as pd
from libraries.strategy.db_StrategyData import update_strategy_database, insert_data_strategy



def on_message(ws, message):
    data = json.loads(message)
    kline = data['k']
    
    if 'k' in data and 'x' in data['k'] and data['k']['x']:
        print('Message received')

    data = {
        'timestamp': kline['t'],
        'open': kline['o'],
        'close': kline['c'],
    }

    # Creating a DataFrame
    new_kline = pd.DataFrame([data])
        
    new_kline['timestamp'] = pd.to_datetime(new_kline['timestamp'], unit='ms')
    new_kline['timestamp'] = new_kline['timestamp'].dt.tz_localize('UTC').dt.tz_convert(TIMEZONE).iloc[0].strftime('%Y-%m-%d %H:%M:%S.%f')
    
    print(f"New Data Frame Received -> Time: {new_kline['timestamp'].iloc[0]}, Open: {new_kline['open'].iloc[0]}, Close: {new_kline['close'].iloc[0]}")
        
        

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Closed with status code", close_status_code, "and message", close_msg)

def on_open(ws):
    print("WebSocket connection opened")    
    

def trade():
    client_UMFutures = connect_to_UMFutures(use_api_keys=True)
    print("Starting bot...")
    print("Bot started...")
    
    socket_url = f"wss://stream.binance.com:9443/ws/{COIN_PAIR.lower()}@kline_{INTERVAL}"
    
    ws = websocket.WebSocketApp(socket_url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open

    try:
        ws.run_forever()
    except KeyboardInterrupt:
        print("WebSocket connection closed due to keyboard interrupt.")
        ws.close()
    



if __name__ == '__main__':
    trade()