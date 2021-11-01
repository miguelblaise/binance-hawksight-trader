
from datetime import datetime
import os
import traceback

from get_emails import connect_inbox, get_mail, parse_body
from binance_api import get_symbol_price, round_down, buy_coins, sell_coins
from send_emails import send_email
from constants import TRADE_COINS

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
SERVER = os.getenv("SERVER")

def buy_sell():
    today = datetime.today()
    # query = '(SUBJECT "Trading signals of Top 12 Cryptocurrency (daily) for Sunday 17 October 2021")'
    query = f'(SUBJECT "Trading signals of Top 12 Cryptocurrency (daily) for {today.strftime("%A %-d %B %Y")}")'

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

    messages = []
    for pair in decision_signals["SELL Signals, profit-optimized:"]:
        order = sell_coins(pair)
        messages.append(order)
    
    for pair in decision_signals["BUY Signals, profit-optimized:"]:
        order = buy_coins(pair)
        messages.append(order)

    return messages

def main():
    receiver = [EMAIL]
    subject = "Hawksight Auto Trader"
    try:
        messages = buy_sell()
        
        body = "Hawksight Auto-Trader Results:<br><br>"
        if not messages:
            return
        for message in messages:
            body += f"<pre style='color:#000000;background:#ffffff;'>{message}</pre><br><br>"
        
    except Exception as e:
        body = f"ERROR:<br><br><pre style='color:#000000;background:#ffffff;'>{traceback.format_exc()}</pre>"

    send_email(receiver, subject, body)

if __name__ == "__main__":
    main()