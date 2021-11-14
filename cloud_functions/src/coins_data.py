import json
import logging
import time

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


def get_supported_coins_ids():
    ref = db.reference(SUPPORTED_COINS)
    return list(ref.get().values())


def get_supported_coins_sym():
    ref = db.reference(SUPPORTED_COINS)
    return list(ref.get().keys())


def get_coins_data(currency):
    try:
        supported_coins = get_supported_coins_ids()
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
            str(date_to_millis_UTC(entry['last_updated'])),
        )
        assets.append(asset)
    return assets


def save_coins_data(assets, path):
    ref = db.reference(path)
    for asset in assets:
        try:
            ref.child(asset.symbol).child(asset.last_updated).set(json.loads(asset.to_json()))
        except Exception as err:
            logging.error(f"An error occured in save_coins_data {err} for {asset}")


def save_coins_data_latest(assets, path):
    ref = db.reference(path)
    for asset in assets:
        try:
            ref.child(asset.symbol).set(json.loads(asset.to_json()))
        except Exception as err:
            logging.error(f"An error occured in save_coins_data_live {err} for {asset}")


def delete_old_data(path, cut_off_time):
    MS_IN_SECONDS = 1000
    supported_coins = get_supported_coins_sym()
    ref = db.reference(path)

    now = round(time.time() * MS_IN_SECONDS)
    cutoff = str(now - cut_off_time).split('.', 1)[0]

    for coin in supported_coins:
        old_items_query = ref.child(coin).order_by_key().end_at(cutoff)
        timestamps = old_items_query.get().keys()
        if timestamps:
            updates = {timestamp: None for timestamp in timestamps}
            try:
                ref.child(coin).update(updates)
            except Exception as err:
                logging.error(f"An error occured in delete_old_data {err} for {coin}")
