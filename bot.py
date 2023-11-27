from libraries.config import TIMEZONE, COIN_PAIR
from libraries.binance.connect import connect_to_spot
from libraries.storage.sql.db_HistoricalData import update_historical_database, insert_data
from libraries.strategy.db_StrategyData import update_strategy_database, insert_data_strategy
from libraries.strategy.main import strategy
from libraries.storage.sql.connect import create_database
import json
import websocket
import pandas as pd


def run_strategy(new_kline, client_trade):
    
    historical_data = insert_data(new_kline)
    strategy_data = strategy(historical_data)
    
    last_row = strategy_data.iloc[-1]
    insert_data_strategy(last_row)

def bot_functions(client):
    create_database()
    
    historical_data = update_historical_database(client)
    update_strategy_database(historical_data)
    
    print("Resynchronizing data...")
    
    historical_data = update_historical_database(client)
    update_strategy_database(historical_data)

def on_message(client_trade, ws, message):
    data = json.loads(message)
    
    if 'k' in data and 'x' in data['k'] and data['k']['x']:
        # Check if the candle is closed (x = True)
        kline = data['k']
        data = {
            'timestamp': kline['t'],
            'open': kline['o'],
            'high': kline['h'],
            'low': kline['l'],
            'close': kline['c'],
            'volume': kline['v']
        }

        # Creating a DataFrame
        new_kline = pd.DataFrame([data])
        
        new_kline['timestamp'] = pd.to_datetime(new_kline['timestamp'], unit='ms')
        new_kline['timestamp'] = new_kline['timestamp'].dt.tz_localize('UTC').dt.tz_convert(TIMEZONE).iloc[0].strftime('%Y-%m-%d %H:%M:%S.%f')
        print(f"New Data Frame Received -> Time: {new_kline['timestamp'].iloc[0]}, Open: {new_kline['open'].iloc[0]}, High: {new_kline['high'].iloc[0]}, Low: {new_kline['low'].iloc[0]}, Close: {new_kline['close'].iloc[0]}, Volume: {new_kline['volume'].iloc[0]}")

        signal = run_strategy(new_kline, client_trade)
        
        

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Closed with status code", close_status_code, "and message", close_msg)

def on_open(ws):
    print("WebSocket connection opened")

def main():
    client_spot = connect_to_spot(use_api_keys=False)
    print("Starting bot...")
    bot_functions(client_spot)
    print("Bot started...")

    INTERVAL = "1m"
    socket_url = f"wss://stream.binance.com:9443/ws/{COIN_PAIR.lower()}@kline_{INTERVAL}"
    
    ws = websocket.WebSocketApp(socket_url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open

    try:
        ws.run_forever()
    except KeyboardInterrupt:
        print("WebSocket connection closed due to keyboard interrupt.")
        ws.close()

if __name__ == "__main__":
    main()
