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

# def round_down(n, d=8):
#     d = int('1' + ('0' * d))
#     return floor(n * d) / d

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
    price = get_symbol_price(client, pair)
    transactions = client.get_my_trades(symbol=pair)
    last_sell_transaction = [transaction for transaction in transactions if not transactions["isBuyer"]][-1]
    quote_qty = last_sell_transaction["quoteQty"]

    order_qty = round_down(client, coin, quote_qty/price)

    order = client.order_market_buy(
        symbol=pair,
        quantity=quantity)
    return order


def sell_coins(pair):
    client = Client(API_KEY, SECRET_KEY)
    price = get_symbol_price(client, pair)
    balance = client.get_asset_balance(asset=pair.replace("USDT", ""))
    

    order_qty = round_down(client, coin, balance/price)

    order = client.order_market_sell(
        symbol=coin,
        quantity=quantity)
    return order


if __name__ == "__main__":
    client = Client(API_KEY, SECRET_KEY)
    coin = "BUSDUSDT"
    price = get_symbol_price(client, coin)
    # balance = float(client.get_asset_balance(asset='XRP')["free"])
    balance = 20
    quantity = round_down(client, coin, balance/price)

    response = client.get_symbol_info(coin)

    print(quantity)
    # order = client.order_market_buy(
    #     symbol=coin,
    #     quantity=quantity)
    # print(order)

    # trades = client.get_all_orders(symbol=coin)
    # print(trades)
    # trades = client.get_my_trades(symbol='XRPBUSD')
    # print(trades)

    balance = client.get_asset_balance(asset='XRP')
    print(balance)