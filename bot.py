from libraries.binance.connect import connect_to_spot
from libraries.binance.connect import connect_to_CMFutures
from libraries.binance.connect import connect_to_UMFutures

from libraries.binance.binance_market import fetch_spot_data




if __name__ == "__main__":
    # Get account and balance information
    client_spot = connect_to_spot(use_api_keys=False)
    # client_CMFutures = connect_to_CMFutures(use_api_keys=True)
    # client_UMFutures = connect_to_UMFutures(use_api_keys=True)
    
    spot_data = fetch_spot_data(client_spot, "BTCUSDT", "1m", 1000)
    print(spot_data)