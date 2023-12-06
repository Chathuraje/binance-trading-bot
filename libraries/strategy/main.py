import pandas as pd
import matplotlib.pyplot as plt
import ta
from libraries.config import RISK_AMOUNT

def strategy(data):
    # Convert 'close' column to numeric
    data['close'] = pd.to_numeric(data['close'], errors='coerce')  # 'coerce' will replace non-numeric values with NaN

    # Drop rows with NaN values
    data = data.dropna()

    # Continue with the rest of your strategy code...

    # Calculate Bollinger Bands
    indicator_bb = ta.volatility.BollingerBands(data['close'], window=14, window_dev=2)
    data['bb_upper'] = indicator_bb.bollinger_hband()
    data['bb_lower'] = indicator_bb.bollinger_lband()
    
    # Calculate Exponential Moving Average
    indicator_ema = ta.trend.EMAIndicator(data['close'], window=100)
    data['ema'] = indicator_ema.ema_indicator()
    
    # Signal generation based on strategy rules
    data['signal'] = 0  # 0 represents no signal

    # Uptrend signal
    data.loc[(data['ema'] < data['bb_lower']), 'signal'] = 1

    # Downtrend signal
    data.loc[(data['ema'] > data['bb_upper']), 'signal'] = -1
    
    # Convert the 'signal' column to integers
    data['signal'] = data['signal'].astype(int)

    # Calculate stop_loss and take_profit based on the RISK_AMOUNT
    # Long trade
    data.loc[data['signal'] == 1, 'stop_loss'] = data['close'] - 200
    data.loc[data['signal'] == 1, 'take_profit'] = data['close'] + 200

    # Short trade
    data.loc[data['signal'] == -1, 'stop_loss'] = data['close'] + 200
    data.loc[data['signal'] == -1, 'take_profit'] = data['close'] - 200

    
    
    data['quantity'] = 0.1
    data['leverage'] = 100

    return data

def exit_strategy(data):
    return data
