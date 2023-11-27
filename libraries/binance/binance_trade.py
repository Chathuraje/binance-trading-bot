



# def __calculate_exit_price(price, signal_type):
#     if signal_type == 1:
#         exit_price = price * (1 + TAKE_PROFIT)
#     elif signal_type == -1:
#         exit_price = price * (1 - STOP_LOSS)
#     else:
#         print("Invalid signal type")
#         exit(1)
        
#     return exit_price


def enter_trade(client, timestamp, signal_type, close_price):
    
    print(f"timestamp: {timestamp}, signal_type: {signal_type}, close_price: {close_price}")
    
    # Get the current balance of the account
    