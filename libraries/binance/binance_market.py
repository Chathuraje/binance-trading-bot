import pandas as pd
from libraries.config import TIMEZONE

def fetch_spot_data(api_client, symbol, interval, limit=1):
    """
    Retrieves the latest spot data for a given trading pair and time interval.

    Parameters:
    - api_client: The API client object for accessing spot data.
    - symbol: The trading pair symbol (e.g., 'BTCUSDT').
    - interval: The time interval for the data (e.g., '1m' for 1 minute).
    - limit: The number of data points to retrieve (default is 1).

    Returns:
    - DataFrame: Pandas DataFrame containing spot data.
    """

    # Check if the limit is within a reasonable range
    if limit > 1000:
        print("Error: Limit must be less than or equal to 1000")
        return None

    try:
        # Retrieve spot data from the API
        klines = api_client.klines(symbol=symbol, interval=interval, limit=limit)
        
        # Convert the data to a Pandas DataFrame for easier manipulation
        spot_data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        spot_data['timestamp'] = pd.to_datetime(spot_data['timestamp'], unit='ms')  # Convert timestamp to datetime
        spot_data['close_time'] = pd.to_datetime(spot_data['close_time'], unit='ms')  # Convert timestamp to datetime

        # Convert timestamp to the configured timezone
        
        spot_data['timestamp'] = spot_data['timestamp'].dt.tz_localize('UTC').dt.tz_convert(TIMEZONE)
        spot_data['close_time'] = spot_data['close_time'].dt.tz_localize('UTC').dt.tz_convert(TIMEZONE)

        # Drop unnecessary columns
        columns_to_drop = ['quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
        spot_data = spot_data.drop(columns=columns_to_drop)

        return spot_data

    except Exception as e:
        # Handle any exceptions and provide a user-friendly error message
        print(f"Error: Unable to fetch spot data - {e}")
        return None
