import json
import logging

from pycoingecko import CoinGeckoAPI

from Asset import Asset
from google.cloud import logging as cloudlogging
from firebase_admin import db

from config import init_credentials, init_database

init_credentials()
init_database()

cg = CoinGeckoAPI()

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
lg_client = cloudlogging.Client()
lg_client.setup_logging(log_level=logging.INFO)


def get_coins_data(currency):
    try:
        ref = db.reference('/')
        supported_coins = ref.child('supported-coingecko').get()
        supported_coins = list(supported_coins.values())
    except Exception as err:
        logging.error(f"An Error occured in get_market_data {err}")
        return None

    return cg.get_coins_markets(vs_currency=currency, ids=supported_coins)


def filter_coins_data(data):
    if data is None:
        logging.warning(f"Empty data provided in filter_market_data")
        return None

    assets = []
    for entry in data:
        asset = Asset(
            entry['id'],
            entry['symbol'],
            entry['name'],
            entry['current_price'],
            entry['market_cap'],
            entry['market_cap_rank'],
            entry['total_volume'],
            entry['high_24h'],
            entry['low_24h'],
            entry['price_change_24h'],
            entry['price_change_percentage_24h'],
            entry['market_cap_change_24h'],
            entry['last_updated'],
        )

        assets.append(asset)
    return assets


def save_coins_data(data, path):
    ref = db.reference(path)
    for asset in data:
        try:
            timestamp = asset.last_updated.split('.', 1)[0]
            ref.child(asset.symbol).child(timestamp).set(json.loads(asset.to_json()))
        except Exception as err:
            logging.error(f"An error occured in save_market_data {err} for {asset}")


def delete_old_data():
    pass
