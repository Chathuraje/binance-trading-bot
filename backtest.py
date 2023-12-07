from libraries.strategy.db_StrategyData import read_data
import pandas as pd

def enter_position(row, equity, leverage, position_type):
    position = position_type
    entry_price = row['close']
    quantity = (equity * leverage) / entry_price
    stop_loss = entry_price - row['stop_loss'] if position_type == 1 else entry_price + row['stop_loss']
    take_profit = entry_price + row['take_profit'] if position_type == 1 else entry_price - row['take_profit']
    return position, entry_price, quantity, stop_loss, take_profit

def exit_position(row, position, entry_price, quantity, equity):
    position = 0
    equity += quantity * (row['close'] - entry_price)
    return position, equity


def calculate_equity(df, initial_equity, initial_leverage, max_trades):
    equity = initial_equity
    leverage = initial_leverage
    position = 0
    entry_price = 0
    stop_loss = 0
    take_profit = 0
    quantity = 0
    open_trades = 0

    equity_over_time = []

    for index, row in df.iterrows():
        if row['signal'] == 1 and position == 0 and open_trades < max_trades:
            position, entry_price, quantity, stop_loss, take_profit = enter_position(row, equity, leverage, position_type=1)
            open_trades += 1
        elif row['signal'] == -1 and position == 0 and open_trades < max_trades:
            position, entry_price, quantity, stop_loss, take_profit = enter_position(row, equity, leverage, position_type=-1)
            open_trades += 1
        elif (row['close'] <= stop_loss or row['close'] >= take_profit) and position != 0:
            position, equity = exit_position(row, position, entry_price, quantity, equity)
            open_trades -= 1
            equity_over_time.append(equity)

    return pd.DataFrame(equity_over_time, columns=['Equity'])

def backtest():
    data = read_data()
    equity_result = calculate_equity(data, 10000, 1, 1)

    print(equity_result)

backtest()
