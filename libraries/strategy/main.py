# --------------------------------------------------------------------------------------------
# Description: Boliger Band, RSI and MA based strategy.
# # Boliger Band - Period: 14 | Deviation: 2
# # Moving Average - Period: 100 | Type: EMA
# --------------------------------------------------------------------------------------------
# Only if the Moving Average is indicates uptrend: When the price crosses the lower Bollinger line, the chart is likely to go up.
# Only if the Moving Average is indicates downtrend: When the price breaks through the uppeer Bollinger line, you can except the chart to go down.
# --------------------------------------------------------------------------------------------

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

    # # Count occurrences of 1 and -1
    # count_buy_signals = (data['signal'] == 1).sum()
    # count_sell_signals = (data['signal'] == -1).sum()

    # print(f"Number of Buy Signals (1): {count_buy_signals}")
    # print(f"Number of Sell Signals (-1): {count_sell_signals}")

    return data


def exit_strategy(data):
    return data