import json
import logging

from firebase_admin import db
from google.cloud import logging as cloudlogging
from pycoingecko import CoinGeckoAPI

from Asset import Asset
from supported_coins import get_supported_coins_ids, get_supported_coins_sym
from time_utils import date_to_millis_UTC, get_current_timestamp_ms

cg = CoinGeckoAPI()

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
lg_client = cloudlogging.Client()
lg_client.setup_logging(log_level=logging.INFO)

SUPPORTED_COINS = '/supported-coingecko'


def get_coins_data(currency):
    try:
        coins = get_supported_coins_ids(SUPPORTED_COINS)
    except Exception as err:
        logging.error(f"An Error occured in get_market_data {err}")
        return None

    return cg.get_coins_markets(vs_currency=currency, ids=coins)


def parse_coins_data(data):
    if data is None:
        logging.warning(f"Empty data provided in parse_coins_data")
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


def parse_coins_data_minimum(data):
    if data is None:
        logging.warning(f"Empty data provided in parse_coins_data")
        return None

    assets = []
    for entry in data:
        asset = Asset(
            symbol=entry['symbol'],
            last_updated=str(date_to_millis_UTC(entry['last_updated'])),
            price=entry['current_price'],
            market_cap=entry['market_cap'],
            total_volume=entry['total_volume']
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
            logging.error(f"An error occured in save_coins_data_latest {err} for {asset}")


def delete_old_coins_data(path, cut_off_time_ms):
    coins = get_supported_coins_sym(SUPPORTED_COINS)
    ref = db.reference(path)

    now_ms = get_current_timestamp_ms()
    cutoff = str(now_ms - cut_off_time_ms).split('.', 1)[0]

    for coin in coins:
        old_items_query = ref.child(coin).order_by_key().end_at(cutoff)
        timestamps = old_items_query.get().keys()
        if timestamps:
            updates = {timestamp: None for timestamp in timestamps}
            try:
                ref.child(coin).update(updates)
            except Exception as err:
                logging.error(f"An error occured in delete_old_data {err} for {coin}")
