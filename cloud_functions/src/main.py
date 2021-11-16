from coins_data import get_coins_data, parse_coins_data, save_coins_data, save_coins_data_latest, delete_old_coins_data
from coins_historical_data import historical_coins_data
from config import init_database
from time_utils import trim_timestamp_to_midnight, get_current_timestamp_ms

SUPPORTED_CURRENCY = 'usd'
LIVE_COINS = '/live-coins'
HISTORICAL_COINS_1D = '/historical-coins-1D'
HISTORICAL_COINS_1M = '/historical-coins-1M'

CUT_OFF_TIME_5D_AGO = 5 * 24 * 60 * 60 * 1000
CUT_OFF_TIME_5Y_AGO = 5 * 365 * 24 * 60 * 60 * 1000

MS_IN_SECOND = 1000
CURRENT_TIMESTAMP = get_current_timestamp_ms()
# GMT 2015-01-01 00:00:00
START_S = 1420070400
END_S = trim_timestamp_to_midnight(CURRENT_TIMESTAMP) // MS_IN_SECOND
init_database()


def execute_coin_batch_1M(event, context):
    assets = get_coins_data(SUPPORTED_CURRENCY)
    assets = parse_coins_data(assets)
    save_coins_data_latest(assets, LIVE_COINS)
    save_coins_data(assets, HISTORICAL_COINS_1M)


def execute_coin_batch_1D(event, context):
    assets = get_coins_data(SUPPORTED_CURRENCY)
    assets = parse_coins_data(assets)
    save_coins_data(assets, HISTORICAL_COINS_1D)


def execute_coin_historical_batch_1D(event, context):
    historical_coins_data(SUPPORTED_CURRENCY, HISTORICAL_COINS_1D, START_S, END_S)


def execute_delete_old_coins_data_5D(event, context):
    delete_old_coins_data(HISTORICAL_COINS_1M, CUT_OFF_TIME_5D_AGO)


def execute_delete_old_coins_data_5Y(event, context):
    delete_old_coins_data(HISTORICAL_COINS_1D, CUT_OFF_TIME_5Y_AGO)
