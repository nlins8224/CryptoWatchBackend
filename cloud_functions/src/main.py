from coins_data import get_coins_data, filter_coins_data, save_coins_data, save_coins_data_latest, delete_old_data

SUPPORTED_CURRENCY = 'usd'
LIVE_COINS = '/live-coins'
HISTORICAL_COINS_1H = '/historical-coins-1H'
HISTORICAL_COINS_1M = '/historical-coins-1M'

CUT_OFF_TIME_5D_AGO = 5 * 24 * 60 * 60 * 1000
CUT_OFF_TIME_5Y_AGO = 5 * 365 * 24 * 60 * 60 * 1000


def execute_coin_batch_1M(event, context):
    assets = get_coins_data(SUPPORTED_CURRENCY)
    assets = filter_coins_data(assets)
    print(assets)
    save_coins_data_latest(assets, LIVE_COINS)
    save_coins_data(assets, HISTORICAL_COINS_1M)


def execute_coin_batch_1H(event, context):
    assets = get_coins_data(SUPPORTED_CURRENCY)
    assets = filter_coins_data(assets)
    print(assets)
    save_coins_data(assets, HISTORICAL_COINS_1H)


def execute_delete_old_data_5D(event, context):
    delete_old_data(HISTORICAL_COINS_1M, CUT_OFF_TIME_5D_AGO)


def execute_delete_old_data_5Y(event, context):
    delete_old_data(HISTORICAL_COINS_1H, CUT_OFF_TIME_5Y_AGO)
