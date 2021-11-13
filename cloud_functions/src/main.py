from coins_data import get_coins_data, filter_coins_data, save_coins_data, save_coins_data_latest

SUPPORTED_CURRENCY = 'usd'
LIVE_COINS = '/live-coins'
HISTORICAL_COINS_1H = '/historical-coins-1H'
HISTORICAL_COINS_1M = '/historical-coins-1M'

# 24 Hours in milliseconds
CUT_OFF_TIME_24H = 24 * 60 * 60 * 1000


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


def execute_delete_old_data_5D():
    pass


def execute_delete_old_data_5Y():
    pass
