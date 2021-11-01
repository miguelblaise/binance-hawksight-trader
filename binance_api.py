import os
from math import floor

from binance.client import Client

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

def get_symbol_price(coin):
    client = Client(API_KEY, SECRET_KEY)
    info = client.get_symbol_ticker()
    for symbol in info:
        if symbol["symbol"] == coin:
            price = symbol["price"]
            print(price)
            return float(price)

def round_down(coin, number):
    client = Client(API_KEY, SECRET_KEY)
    info = client.get_symbol_info(coin)
    step_size = [float(_['stepSize']) for _ in info['filters'] if _['filterType'] == 'LOT_SIZE'][0]
    step_size = '%.8f' % step_size
    step_size = step_size.rstrip('0')
    decimals = len(step_size.split('.')[1])
    return floor(number * 10 ** decimals) / 10 ** decimals

def buy_coins(pair):
    client = Client(API_KEY, SECRET_KEY)
    price = get_symbol_price(pair)
    transactions = client.get_my_trades(symbol=pair)
    last_transaction = [transaction for transaction in transactions][-1]

    if last_transaction["isBuyer"]:
        print(f"{pair}: last transaction was buy. Skip buy.")
        return
    
    quote_qty = float(last_transaction["quoteQty"])

    order_qty = round_down(pair, quote_qty/price)

    order = client.order_market_buy(
        symbol=pair,
        quantity=order_qty)
    return order


def sell_coins(pair):
    client = Client(API_KEY, SECRET_KEY)
    price = get_symbol_price(pair)
    balance = float(client.get_asset_balance(asset=pair.replace("USDT", ""))["free"])

    info = client.get_symbol_info(pair)
    min_notional = [float(_['minNotional']) for _ in info['filters'] if _['filterType'] == 'MIN_NOTIONAL'][0]
    

    order_qty = round_down(pair, balance/price)
    if order_qty <= min_notional:
        print(f"{pair}: Total qty less than min sell qty")
        return

    order = client.order_market_sell(
        symbol=pair,
        quantity=order_qty)
    return order


if __name__ == "__main__":
    client = Client(API_KEY, SECRET_KEY)
    coin = "BUSDUSDT"
    price = get_symbol_price(coin)
    # balance = float(client.get_asset_balance(asset='XRP')["free"])
    balance = 20
    quantity = round_down(coin, balance/price)

    response = client.get_symbol_info(coin)

    print(response)
    # order = client.order_market_buy(
    #     symbol=coin,
    #     quantity=quantity)
    # print(order)

    # trades = client.get_all_orders(symbol=coin)
    # print(trades)
    # trades = client.get_my_trades(symbol='XRPUSDT')
    # print(trades)

    balance = client.get_asset_balance(asset='XRP')
    print(balance)