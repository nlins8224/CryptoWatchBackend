import json
import logging

from firebase_admin import db
from google.cloud import logging as cloudlogging
from pycoingecko import CoinGeckoAPI

from Asset import Asset
from config import init_credentials, init_database
from date_to_millis_UTC import date_to_millis_UTC

init_credentials()
init_database()

cg = CoinGeckoAPI()

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
lg_client = cloudlogging.Client()
lg_client.setup_logging(log_level=logging.INFO)

SUPPORTED_COINS = '/supported-coingecko'


def get_coins_data(currency):
    try:
        ref = db.reference(SUPPORTED_COINS)
        supported_coins = list(ref.get().values())
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
            date_to_millis_UTC(entry['last_updated']),
        )
        assets.append(asset)
    return assets


def save_coins_data(data, path):
    ref = db.reference(path)
    for asset in data:
        try:
            timestamp = asset.last_updated
            ref.child(asset.symbol).child(timestamp).set(json.loads(asset.to_json()))
        except Exception as err:
            logging.error(f"An error occured in save_coins_data {err} for {asset}")


def save_coins_data_latest(data, path):
    ref = db.reference(path)
    for asset in data:
        try:
            ref.child(asset.symbol).set(json.loads(asset.to_json()))
        except Exception as err:
            logging.error(f"An error occured in save_coins_data_live {err} for {asset}")


def delete_old_data(path, cut_off_time):
    pass
