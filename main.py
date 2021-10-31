
from datetime import datetime
import os

from get_emails import connect_inbox, get_mail, parse_body
from binance_api import get_symbol_price, round_down, buy_coins, sell_coins
from constants import TRADE_COINS

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
SERVER = os.getenv("SERVER")

def main():
    today = datetime.today()
    # query = '(SUBJECT "Trading signals of Top 12 Cryptocurrency (daily) for Sunday 17 October 2021")'
    query = f'(SUBJECT "Trading signals of Top 12 Cryptocurrency (daily) for {today.strftime("%A %d %B %Y")}")'

    mail = connect_inbox(EMAIL, PASSWORD, SERVER)
    mail_from, mail_subject, message = get_mail(mail, query)

    signals = parse_body(message)
    signal_keys = [
        "SELL Signals, profit-optimized:",
        "BUY Signals, profit-optimized:",
    ]

    decision_signals = {}
    for key in signal_keys:
        try:
            decision_signals[key] = [
                signal.replace('/','') for signal in signals[key] if signal.replace('/','') in TRADE_COINS
                ]
        except KeyError:
            decision_signals[key] = []
    orders = [] 
    for pair in decision_signals["SELL Signals, profit-optimized:"]:
        order = sell_coins(pair)
        orders.append(order)
    
    for pair in decision_signal["BUY Signals, profit-optimized:"]:
        order = buy_coins(pair)
        orders.append(order)

    return orders

if __name__ == "__main__":
    signals = main()
    print(signals)
    # print(buy)