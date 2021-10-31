import os
from math import floor

from binance.client import Client

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

def get_symbol_price(client, coin):
    info = client.get_symbol_ticker()
    for symbol in info:
        if symbol["symbol"] == coin:
            price = symbol["price"]
            print(price)
            return float(price)

# def round_down(n, d=8):
#     d = int('1' + ('0' * d))
#     return floor(n * d) / d

def round_down(client, coin, number):
    info = client.get_symbol_info(coin)
    step_size = [float(_['stepSize']) for _ in info['filters'] if _['filterType'] == 'LOT_SIZE'][0]
    step_size = '%.8f' % step_size
    step_size = step_size.rstrip('0')
    decimals = len(step_size.split('.')[1])
    return floor(number * 10 ** decimals) / 10 ** decimals

if __name__ == "__main__":
    client = Client(API_KEY, SECRET_KEY)
    coin = "XRPBUSD"
    price = get_symbol_price(client, coin)
    # quantity = format(round_down(20/price, 4), '.8f')\
    quantity = round_down(client, coin, 20/price)

    response = client.get_symbol_info(coin)

    print(quantity)
    order = client.order_market_buy(
        symbol=coin,
        quantity=quantity)

