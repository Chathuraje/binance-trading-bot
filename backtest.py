import pandas as pd
import backtrader as bt
from libraries.strategy.db_StrategyData import read_data

class MyStrategy(bt.Strategy):
    params = (
        ("leverage", 1),  # Default leverage
        ("stop_loss", 0.02),  # Default stop-loss as a percentage
        ("take_profit", 0.02),  # Default take-profit as a percentage
    )

    def __init__(self):
        self.order = None

    def next(self):
        if self.order:
            return  # If an order is pending, don't do anything

        timestamp = self.data.datetime.datetime()
        close = self.data.close[0]
        signal = self.data.signal[0]
        leverage = self.params.leverage
        stop_loss = close * (1 - self.params.stop_loss)
        take_profit = close * (1 + self.params.take_profit)
        quantity = self.data.quantity[0]

        if signal == 1:
            self.order = self.buy(size=quantity, exectype=bt.Order.Stop, price=stop_loss)
            self.sell(exectype=bt.Order.Limit, price=take_profit, parent=self.order)
        elif signal == -1:
            self.order = self.sell(size=quantity, exectype=bt.Order.Stop, price=stop_loss)
            self.buy(exectype=bt.Order.Limit, price=take_profit, parent=self.order)

    def notify_order(self, order):
        if order.status in [order.Completed, order.Canceled, order.Margin, order.Rejected]:
            if order.isbuy():
                self.log(f"Buy executed - Price: {order.executed.price}, Cost: {order.executed.value}, Comm: {order.executed.comm}")
            elif order.issell():
                self.log(f"Sell executed - Price: {order.executed.price}, Cost: {order.executed.value}, Comm: {order.executed.comm}")

            self.order = None

def backtest():
    cerebro = bt.Cerebro()

    # Add the data to the backtest
    data = read_data()
    data['timestamp'] = pd.to_datetime(data['timestamp'])  # Convert timestamp to datetime
    data = bt.feeds.PandasData(dataname=data.set_index('timestamp'))
    cerebro.adddata(data)

    # Add the strategy to the backtest
    cerebro.addstrategy(MyStrategy)

    # Set the initial cash amount
    cerebro.broker.set_cash(10000)

    # Print the starting cash amount
    print(f"Starting Portfolio Value: {cerebro.broker.getvalue()}")

    # Run the backtest
    cerebro.run()

    # Print the final cash amount
    print(f"Ending Portfolio Value: {cerebro.broker.getvalue()}")

if __name__ == '__main__':
    backtest()
