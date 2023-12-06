from libraries.strategy.db_StrategyData import read_data


def backtest():
    data = read_data()
    
    print(data)
    
    
    
    
    
if __name__ == '__main__':
    backtest()