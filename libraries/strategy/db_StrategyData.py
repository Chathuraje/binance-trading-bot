from libraries.storage.sql.connect import connect_sqlalchemy
import pandas as pd
from libraries.binance.market import fetch_spot_data
from libraries.config import COIN_PAIR, INTERVAL
from libraries.strategy.main import strategy

    
def insert_data_strategy(row):
    db = connect_sqlalchemy()

    # Check if the timestamp already exists in the database
    timestamp_value = row['timestamp']  # Extract scalar value from the pandas Series
    existing_timestamp = pd.read_sql(
        "SELECT timestamp FROM StrategyData WHERE timestamp = :timestamp",
        con=db, params={'timestamp': timestamp_value}
    )

    if existing_timestamp.empty:
        # Save the new data to the database
        row_df = pd.DataFrame([row[['timestamp', 'close', 'bb_upper', 'bb_lower', 'ema', 'signal']]]) # Select relevant columns
        row_df.to_sql('StrategyData', con=db, if_exists='append', index=False)

    # Close the database connection
    db.dispose()

    return read_data()
    
    
    
def read_data():
    # Connect to the database
    db = connect_sqlalchemy()

    # Define the SQL query to retrieve data from the 'historical_data' table
    query = "SELECT * FROM StrategyData"

    # Use pandas to read the data from the database into a DataFrame
    data = pd.read_sql(query, con=db)

    # Close the database connection
    db.dispose()

    return data

def update_strategy_database(historical_data):
    try:
        data = strategy(historical_data)

        # Drop unnecessary columns
        columns_to_drop = ['open', 'high', 'low', 'volume']
        data = data.drop(columns=columns_to_drop)

        strategy_data = update_data(data)
        
        return strategy_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # or handle the error in an appropriate way


def update_data(data):
    db = connect_sqlalchemy()

    # Retrieve existing timestamps from the database
    existing_timestamps = pd.read_sql("SELECT DISTINCT timestamp FROM StrategyData", con=db)['timestamp']

    # Filter the new data to include only rows with timestamps not present in the database
    new_data = data[~data['timestamp'].isin(existing_timestamps)]

    if not new_data.empty:
        # Save the new data to the database
        new_data.to_sql('StrategyData', con=db, if_exists='append', index=False)

    # Close the database connection
    db.dispose()

    return read_data()
    