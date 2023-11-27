from libraries.config import TIMEZONE, INTERVAL, COIN_PAIR
from libraries.binance.connect import connect_to_spot
from libraries.storage.sql.db_HistoricalData import update_historical_database, create_database, update_data, read_data
from libraries.strategy.main import strategy
import json
import websocket
import pandas as pd


csv_file_path = 'libraries/storage/local/kline_data.csv'
historical_data = []



def run_strategy():
    global historical_data
    latest_data = pd.read_csv(csv_file_path)
    
    merged_data = pd.concat([historical_data, latest_data], ignore_index=True)
    strategy_data = strategy(merged_data)
    
    
    last_row = strategy_data.iloc[-1]
    last_signal = int(last_row['signal'])
    timestamp = last_row['timestamp']
    close_price = last_row['close']

    signal_messages = {
        0: "No Signal",
        1: "Buy Signal (Enter Long)",
        -1: "Sell Signal (Enter Short)"
    }

    signal_message = signal_messages.get(last_signal, "Unknown Signal")
    
    print(f"At {timestamp} ({INTERVAL}), Close Price: {close_price:.2f} - {signal_message}")
    
    
    return strategy_data


def __update_local_storage():
    try:
        df = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        # Always create a new empty CSV file with headers
        df.to_csv(csv_file_path, index=False)
        print("Empty CSV file created.")
    except Exception as e:
        print("Error creating CSV file:", e)
    

def bot_functions(client):
    global historical_data
    
    __update_local_storage()
    create_database()
    historical_data = update_historical_database(client)
    

def on_message(ws, message):
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
        new_kline['timestamp'] = new_kline['timestamp'].dt.tz_localize('UTC').dt.tz_convert(TIMEZONE)
        
        print(f"New Data Frame Received -> Time: {new_kline['timestamp'].iloc[0].strftime('%Y-%m-%d %H:%M:%S')}, Open: {kline['o']}, High: {kline['h']}, Low: {kline['l']}, Close: {kline['c']}, Volume: {kline['v']}")
        new_kline.to_csv(csv_file_path, mode='a', header=False, index=False, sep=',', date_format='%Y-%m-%d %H:%M:%S.%f')
        
        run_strategy()
        
        

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

    # INTERVAL = "1s"
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
