from libraries.binance.connect import connect_to_spot
from libraries.binance.connect import connect_to_CMFutures
from libraries.binance.connect import connect_to_UMFutures

from libraries.binance.market import fetch_spot_data


from libraries.config import COIN_PAIR, INTERVAL



if __name__ == "__main__":
    # Get account and balance information
    client_spot = connect_to_spot(use_api_keys=False)
    # client_CMFutures = connect_to_CMFutures(use_api_keys=True)
    # client_UMFutures = connect_to_UMFutures(use_api_keys=True)

    start_time = "2023-10-01 00:00:00"
    end_time = "2023-10-01 23:59:59"
    
    spot_data = fetch_spot_data(client_spot, COIN_PAIR, INTERVAL)
    print(spot_data)
    
    # print(get_historical_data())
    