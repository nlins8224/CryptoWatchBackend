import json
import logging

from firebase_admin import db
from google.cloud import logging as cloudlogging
from pycoingecko import CoinGeckoAPI

from Asset import Asset
from get_supported_coins import get_supported_coins_ids, get_supported_coins_sym

cg = CoinGeckoAPI()

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
lg_client = cloudlogging.Client()
lg_client.setup_logging(log_level=logging.INFO)

SUPPORTED_COINS = '/supported-coingecko'


def get_historical_coin_data(coin, vs_currency, days):
    return cg.get_coin_market_chart_by_id(id=coin, vs_currency=vs_currency, days=days)


def parse_historical_coin_data(data, coin_symbol):
    if data is None:
        logging.warning(f"Empty data provided in parse_historical_coin_data")
        return None

    prices = data['prices']
    market_caps = data['market_caps']
    total_volumes = data['total_volumes']
    assets = dict()

    for price, market, volume in zip(prices, market_caps, total_volumes):
        if price[0] == market[0] and market[0] == volume[0]:
            asset = Asset(
                symbol=coin_symbol,
                last_updated=price[0],
                price=price[1],
                market_cap=market[1],
                total_volume=volume[1]
            )
            assets[price[0]] = json.loads(asset.to_json())
    return assets


def historical_coins_data(currency, days, path):
    try:
        coins = get_supported_coins_ids(SUPPORTED_COINS)
        coins_symbols = get_supported_coins_sym(SUPPORTED_COINS)

        coin_id_symbol_map = dict(zip(coins, coins_symbols))

        for coin in coins:
            coin_symbol = coin_id_symbol_map[coin]

            data = get_historical_coin_data(coin, currency, days)
            data = parse_historical_coin_data(data, coin_symbol)
            save_historical_coin_data(data, path, coin_symbol)
    except Exception as err:
        logging.error(f"An Error occured in get_historical_coins_data {err}")


def save_historical_coin_data(data, path, coin_symbol):
    ref = db.reference(path)
    try:
        ref.child(coin_symbol).update(data)
        logging.info(f"Saved {coin_symbol} historical data in {path}/{coin_symbol}")
    except Exception as err:
        logging.error(f"An error occured in save_historical_coin_data {err}")
