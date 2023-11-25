# Importing necessary modules from the Binance API
from binance.spot import Spot
from binance.cm_futures import CMFutures
from binance.um_futures import UMFutures

# Importing API keys from a configuration file
from .config import BINANCE_API_KEY, BINANCE_SECRET_KEY

def connect_to_binance(api_class, name, use_api_keys=True):
    """
    Connects to the Binance API using the provided API class.

    Args:
        api_class (class): The Binance API class (Spot, CMFutures, UMFutures).
        name (str): The name of the API class for logging purposes.
        use_api_keys (bool): Indicates whether to use API keys or not.

    Returns:
        client: The connected Binance API client.
    """
    try:
        # Creating an instance of the specified Binance API class
        if use_api_keys:
            if api_class == Spot:
                client = api_class(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY)
            else:
                client = api_class(key=BINANCE_API_KEY, secret=BINANCE_SECRET_KEY)
            
            client.ping()
            print(f"Connecting to Binance {name} API successful")
            
        else:
            client = api_class()
            client.ping()
            
            print(f"Connecting to Binance {name} successful")
            
        # Pinging the Binance server to ensure a successful connection
        return client
    except Exception as e:
        # Handling connection errors and exiting the program
        print(e)
        print("Failed to connect to Binance API")
        exit(1)

def connect_to_spot(use_api_keys=True):
    """
    Connects to the Binance Spot API.

    Args:
        use_api_keys (bool): Indicates whether to use API keys or not.

    Returns:
        Spot: The connected Binance Spot API client.
    """
    return connect_to_binance(Spot, "Spot", use_api_keys)

def connect_to_CMFutures(use_api_keys=True):
    """
    Connects to the Binance Coin-M Futures API.

    Args:
        use_api_keys (bool): Indicates whether to use API keys or not.

    Returns:
        CMFutures: The connected Binance Coin-M Futures API client.
    """
    return connect_to_binance(CMFutures, "CMFutures", use_api_keys)

def connect_to_UMFutures(use_api_keys=True):
    """
    Connects to the Binance USD-M Futures API.

    Args:
        use_api_keys (bool): Indicates whether to use API keys or not.

    Returns:
        UMFutures: The connected Binance USD-M Futures API client.
    """
    return connect_to_binance(UMFutures, "UMFutures", use_api_keys)
