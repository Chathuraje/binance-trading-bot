from .connect import connect_sqlalchemy
import pandas as pd
from libraries.binance.market import fetch_spot_data
from libraries.config import COIN_PAIR, INTERVAL

def insert_data(row):
    db = connect_sqlalchemy()

    # Check if the timestamp already exists in the database
    timestamp_value = row['timestamp'].iloc[0]  # Extract scalar value from the pandas Series
    existing_timestamp = pd.read_sql(
        "SELECT timestamp FROM HistoricalData WHERE timestamp = :timestamp",
        con=db, params={'timestamp': timestamp_value}
    )

    if existing_timestamp.empty:
        # Save the new data to the database
        row_df = row[['timestamp', 'open', 'high', 'low', 'close', 'volume']]  # Select relevant columns
        row_df.to_sql('HistoricalData', con=db, if_exists='append', index=False)

    # Close the database connection
    db.dispose()

    return read_data()


    
    
def read_data():
    # Connect to the database
    db = connect_sqlalchemy()

    # Define the SQL query to retrieve data from the 'historical_data' table
    query = "SELECT * FROM HistoricalData"

    # Use pandas to read the data from the database into a DataFrame
    data = pd.read_sql(query, con=db)

    # Close the database connection
    db.dispose()

    return data


def __find_last_timeframe():
    db = connect_sqlalchemy()
    
    # Define the SQL query to retrieve data from the 'historical_data' table
    query = "SELECT * FROM HistoricalData ORDER BY timestamp DESC LIMIT 1"

    # Use pandas to read the data from the database into a DataFrame
    data = pd.read_sql(query, con=db)

    # Close the database connection
    db.dispose()
    
    if data.empty:
        timestamp_value = "2017-08-17 04:00:00"
    else:
        # Extract the timestamp from the DataFrame and convert it to the desired format
        timestamp_value = data['timestamp'].values[0]
    
    
    formatted_timestamp = pd.to_datetime(timestamp_value).strftime("%Y-%m-%d %H:%M:%S")
    
    last_timeframe_datetime = pd.to_datetime(formatted_timestamp)
    
     # Add the specified interval to the last timeframe
    new_timeframe_datetime = last_timeframe_datetime + pd.to_timedelta(INTERVAL)

    # Convert the new timeframe back to the desired format
    next_timeframe = new_timeframe_datetime.strftime("%Y-%m-%d %H:%M:%S")

    return next_timeframe
    

def update_historical_database(client_spot):
    last_timeframe = __find_last_timeframe()
    latest_data = fetch_spot_data(client_spot, COIN_PAIR, INTERVAL, start_time=last_timeframe)
    
    # Remove the last row from the DataFrame
    data_without_last_row = latest_data.iloc[:-1]
    
    data = update_data(data_without_last_row)
    
    return data


def update_data(data):
    db = connect_sqlalchemy()
    
    # Check if data is empty
    if data.empty:
        return read_data()

    # Retrieve existing timestamps from the database
    existing_timestamps = pd.read_sql("SELECT DISTINCT timestamp FROM HistoricalData", con=db)['timestamp']

    # Filter the new data to include only rows with timestamps not present in the database
    new_data = data[~data['timestamp'].isin(existing_timestamps)]

    if not new_data.empty:
        # Save the new data to the database
        new_data.to_sql('HistoricalData', con=db, if_exists='append', index=False)

    # Close the database connection
    db.dispose()

    return read_data()
    