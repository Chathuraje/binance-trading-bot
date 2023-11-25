from libraries.binance.connect import connect_to_spot
from libraries.binance.connect import connect_to_CMFutures
from libraries.binance.connect import connect_to_UMFutures




if __name__ == "__main__":
    # Get account and balance information
    client_spot = connect_to_spot(use_api_keys=False)
    client_CMFutures = connect_to_CMFutures(use_api_keys=True)
    client_UMFutures = connect_to_UMFutures(use_api_keys=True)
    
    