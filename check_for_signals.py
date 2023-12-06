import time
import pandas as pd
from libraries.strategy.db_StrategyData import get_last_timstamp, read_last_record
from libraries.binance.binance_trade import enter_trade
from libraries.storage.mongodb.db_TradeData import get_active_trade_count
from libraries.binance.connect import connect_to_UMFutures
from libraries.config import MARKET, FIAT_CURRENCY, MINUMUM_ACCOUNT_BALANCE, COIN_PAIR, MAX_ORDERS

# Global variable to store the last processed timestamp
last_processed_timestamp = pd.to_datetime(get_last_timstamp())

def update_last_processed_timestamp(timestamp):
    # Implement a function to update the timestamp of the last processed signal in a configuration file, database, or any other storage.
    global last_processed_timestamp
    last_processed_timestamp = timestamp

def check_for_signals(client, tick_size, precision):
    global last_processed_timestamp
    
    while True:
        # Fetch the latest signal from the database
        latest_signal = read_last_record()

        if latest_signal is not None:
            # Get the timestamp of the latest signal
            latest_timestamp = pd.to_datetime(latest_signal['timestamp'].iloc[0])

            # Compare with the last processed timestamp
            if latest_timestamp > last_processed_timestamp:
                # Extract relevant information from the signal
                timestamp = latest_timestamp
                
                if latest_signal['signal'].iloc[0] == 0:
                    print(f"No signal at {timestamp}")
                elif latest_signal['signal'].iloc[0] == 1 or latest_signal['signal'].iloc[0] == -1:
                
                    if get_active_trade_count() >= int(MAX_ORDERS):
                        print(f"New Signal Received: Given {MAX_ORDERS} Orders are Active")
                    else:
                        enter_trade(client, timestamp, latest_signal, tick_size, precision)
                        
                else:
                    print(f"Invalid signal at {timestamp}")
                
                # Update the timestamp of the last processed signal
                update_last_processed_timestamp(timestamp)

        # Sleep for 1 second before checking for new signals again
        time.sleep(1)



def __get_account_balance(client):
    data = client.account()
    balance = next(asset['availableBalance'] for asset in data['assets'] if asset['asset'] == FIAT_CURRENCY)

    return balance


def __select_the_market():
    if MARKET == "UMFutures":
        client = connect_to_UMFutures(use_api_keys=True)
    else:
        print("Invalid Market")
        exit(1)
        
    return client

def __get_tick_size(client):
    try:
        data = client.exchange_info()
         # Assuming you want to get tick size for the first symbol
        tick_size = float(data['symbols'][0]['filters'][0]['tickSize'])
        precision = int(data['symbols'][0]['filters'][0]['tickSize'].split('.')[1].find('1'))
        
        return tick_size, precision
    except:
        print("Failed to get exchange info")
        exit(1)
   


def __setup_account(client):
    if MARKET == "CMFutures" or MARKET == "UMFutures":
        try:
            client.change_position_mode(dualSidePosition=True) # change position mode to Hedge Mode
        except:
            print(f"Failed to change position mode to Hedge Mode or current position mode is already Hedge Mode")
        
        try:
            client.change_margin_type(symbol=COIN_PAIR, marginType='CROSSED')
        except:
            print(f"Failed to change margin type to CROSSED or current margin type is already CROSSED")
            
    else:
        print("Invalid Market")
        exit(1)

if __name__ == "__main__":
    print("Starting the Bot..")
    client = __select_the_market()
    
    tick_size, precision = __get_tick_size(client)
    
    account_balance = __get_account_balance(client)
    __setup_account(client)
    
    print(f"The available Balance for {FIAT_CURRENCY} is: {account_balance}")
    
    if MINUMUM_ACCOUNT_BALANCE > account_balance:
        print("Insufficient Balance")
        exit(1)
    
    print("Starting to check for signals...")
    check_for_signals(client, tick_size, precision)
