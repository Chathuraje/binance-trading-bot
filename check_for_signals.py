import time
import pandas as pd
from libraries.strategy.db_StrategyData import get_last_timstamp, read_last_record
from libraries.binance.binance_trade import enter_trade
from libraries.binance.connect import connect_to_UMFutures, connect_to_CMFutures, connect_to_spot
from libraries.config import MARKET, FIAT_CURRENCY, MINUMUM_ACCOUNT_BALANCE
import json

# Global variable to store the last processed timestamp
last_processed_timestamp = pd.to_datetime(get_last_timstamp())

def update_last_processed_timestamp(timestamp):
    # Implement a function to update the timestamp of the last processed signal in a configuration file, database, or any other storage.
    global last_processed_timestamp
    last_processed_timestamp = timestamp

def check_for_signals(client):
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
                signal_type = latest_signal['signal'].iloc[0]
                close_price = latest_signal['close'].iloc[0]
                # Add any other relevant fields


                if latest_signal['signal'].iloc[0] == 0:
                    print(f"No signal at {timestamp}")
                elif latest_signal['signal'].iloc[0] == 1 or latest_signal['signal'].iloc[0] == -1:
                    # Execute trade based on the signal
                    enter_trade(client, timestamp, signal_type, close_price)
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
    if MARKET == "Spot":
        client = connect_to_spot(use_api_keys=True)
    elif MARKET == "CMFutures":
        client = connect_to_CMFutures(use_api_keys=True)
    elif MARKET == "UMFutures":
        client = connect_to_UMFutures(use_api_keys=True)
    else:
        print("Invalid Market")
        exit(1)
        
    return client

if __name__ == "__main__":
    print("Starting the Bot..")
    client = __select_the_market()
    account_balance = __get_account_balance(client)
    
    print(f"The available Balance for {FIAT_CURRENCY} is: {account_balance}")
    
    if MINUMUM_ACCOUNT_BALANCE > account_balance:
        print("Insufficient Balance")
        exit(1)
    
    print("Starting to check for signals...")
    check_for_signals(client)
