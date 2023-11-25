import ccxt

def get_historical_data():
    binance = ccxt.binance()
    ticker = binance.fetch_ticker('BTC/USDT')
    print(ticker)