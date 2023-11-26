import pandas as pd
from tqdm import tqdm
from libraries.config import TIMEZONE
from datetime import datetime, timedelta
import pytz 

# Function to convert a time string to milliseconds
def __convert_to_milliseconds(time_string):
    """
    Converts a time string to milliseconds.

    Parameters:
    - time_string (str): The time string in the format '%Y-%m-%d %H:%M:%S'.

    Returns:
    - int or None: The time in milliseconds or None if no time_string is provided.
    """
    if time_string:
        return pd.to_datetime(time_string, format='%Y-%m-%d %H:%M:%S').tz_localize(TIMEZONE).value // 10**6
    else:
        return None

# Function to calculate the total number of timeframes between start and end times based on a given interval
def __calculate_total_timeframes(start_time, end_time, interval):
    """
    Calculates the total number of timeframes between start and end times based on a given interval.

    Parameters:
    - start_time (str): The start time in the format '%Y-%m-%d %H:%M:%S'.
    - end_time (str): The end time in the format '%Y-%m-%d %H:%M:%S'.
    - interval (str): The time interval for each timeframe.

    Returns:
    - int: The total number of timeframes.
    """
    start_time_ms = __convert_to_milliseconds(start_time)
    end_time_ms = __convert_to_milliseconds(end_time)
    
    time_difference = (end_time_ms - start_time_ms) / (pd.to_timedelta(interval).total_seconds() * 1000)
    return int(time_difference)

# Function to fetch klines (candlestick data) from an API
def __fetch_klines(api_client, symbol, interval, start_time_ms, end_time_ms, limit):
    # start_time = "2017-08-17 04:00:00" # First Record in Binance 
    """
    Fetches klines (candlestick data) from the API within a specified time range.

    Parameters:
    - api_client: The API client object.
    - symbol (str): The trading symbol.
    - interval (str): The time interval for each candlestick.
    - start_time_ms (int): The start time in milliseconds.
    - end_time_ms (int): The end time in milliseconds.
    - limit (int): The maximum number of klines to fetch.

    Returns:
    - list: List of klines data.
    """
    return api_client.klines(symbol=symbol, interval=interval, startTime=start_time_ms, endTime=end_time_ms, limit=limit)

# Function to process klines data and convert it to a Pandas DataFrame
def __process_klines(klines):
    """
    Processes raw klines data and converts it to a Pandas DataFrame.

    Parameters:
    - klines (list): List of raw klines data.

    Returns:
    - pd.DataFrame: Processed klines data in a DataFrame.
    """
    spot_data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    
    # Convert timestamp to datetime, localize to UTC, and convert to the specified TIMEZONE
    spot_data['timestamp'] = pd.to_datetime(spot_data['timestamp'], unit='ms')
    spot_data['timestamp'] = spot_data['timestamp'].dt.tz_localize('UTC').dt.tz_convert(TIMEZONE)

    # Drop unnecessary columns
    columns_to_drop = ['close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
    spot_data = spot_data.drop(columns=columns_to_drop)

    return spot_data

# Function to fetch spot data within a specified time range
def fetch_spot_data(api_client, symbol, interval, start_time=None, end_time=None, limit=1000, total_records=None):
    """
    Fetches spot data within a specified time range using an API client.

    Parameters:
    - api_client: The API client object.
    - symbol (str): The trading symbol.
    - interval (str): The time interval for each candlestick.
    - start_time (str): The start time in the format '%Y-%m-%d %H:%M:%S'.
    - end_time (str): The end time in the format '%Y-%m-%d %H:%M:%S'.
    - limit (int): The maximum number of klines to fetch in each API call.
    - total_records (int): The total number of records to fetch.

    Returns:
    - pd.DataFrame: Combined spot data in a DataFrame.
    """
    try:
        # Set start_time to today's start time if it is None
        if start_time is None:
            start_time = datetime.now(pytz.timezone(TIMEZONE)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')

        # Set end_time to the current time if it is None
        if end_time is None:
            # Get the current time in the specified TIMEZONE
            current_time = datetime.now(pytz.timezone(TIMEZONE)).strftime('%Y-%m-%d %H:%M:%S')
            end_time = current_time
            
        # Calculate the total number of timeframes to fetch
        if total_records is None:
            total_timeframes = __calculate_total_timeframes(start_time, end_time, interval)
        else:
            total_timeframes = total_records
        
        print(f"Total timeframes to fetch: {total_timeframes}")

        # Convert start and end times to milliseconds
        start_time_ms = __convert_to_milliseconds(start_time)
        end_time_ms = __convert_to_milliseconds(end_time)

        combined_data = pd.DataFrame()

        # Use tqdm for progress tracking
        with tqdm(total=(total_records // limit) if total_records else int(total_timeframes / limit), desc="Fetching Spot Data", unit="timeframes", position=0, leave=True) as pbar:
            count = 0
            while start_time_ms < end_time_ms:
                # Fetch klines data
                klines = __fetch_klines(api_client, symbol, interval, start_time_ms, end_time_ms, limit)
                if not klines:
                    break

                # Process klines data
                spot_data = __process_klines(klines)

                # Handle the case when a specific number of records is requested
                if total_records is not None:
                    remaining_records = total_records - len(combined_data)
                    spot_data = spot_data.head(remaining_records)

                # Concatenate data to the combined DataFrame
                combined_data = pd.concat([combined_data, spot_data], ignore_index=True)

                count += 1
                pbar.update(1)
                pbar.refresh()

                # Update the start time for the next iteration
                start_time_ms = spot_data['timestamp'].max().value // 10**6 + 1

                # Exit the loop if the required number of records is reached
                if total_records is not None and len(combined_data) >= total_records:
                    break

        return combined_data

    except Exception as e:
        # Handle any exceptions that may occur during the process
        print(f"Error: Unable to fetch spot data - {e}")
        return None
