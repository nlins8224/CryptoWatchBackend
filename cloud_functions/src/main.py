from coins_data import get_coins_data, filter_coins_data, save_coins_data, save_coins_data_latest, delete_old_coins_data
from coins_historical_data import historical_coins_data
from config import init_database

SUPPORTED_CURRENCY = 'usd'
LIVE_COINS = '/live-coins'
HISTORICAL_COINS_1D = '/historical-coins-1D'
HISTORICAL_COINS_1M = '/historical-coins-1M'

CUT_OFF_TIME_5D_AGO = 5 * 24 * 60 * 60 * 1000
CUT_OFF_TIME_5Y_AGO = 5 * 365 * 24 * 60 * 60 * 1000

DAYS = 'max'

init_database()


def execute_coin_batch_1M(event, context):
    assets = get_coins_data(SUPPORTED_CURRENCY)
    assets = filter_coins_data(assets)
    print(assets)
    save_coins_data_latest(assets, LIVE_COINS)
    save_coins_data(assets, HISTORICAL_COINS_1M)


def execute_coin_batch_1D(event, context):
    assets = get_coins_data(SUPPORTED_CURRENCY)
    assets = filter_coins_data(assets)
    print(assets)
    save_coins_data(assets, HISTORICAL_COINS_1D)


def execute_coin_historical_batch_1D(event, context):
    historical_coins_data(SUPPORTED_CURRENCY, DAYS, HISTORICAL_COINS_1D)


def execute_delete_old_coins_data_5D(event, context):
    delete_old_coins_data(HISTORICAL_COINS_1M, CUT_OFF_TIME_5D_AGO)


def execute_delete_old_coins_data_5Y(event, context):
    delete_old_coins_data(HISTORICAL_COINS_1D, CUT_OFF_TIME_5Y_AGO)
