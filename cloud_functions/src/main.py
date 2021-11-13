from coins_data import get_coins_data, filter_coins_data, save_coins_data_live, save_coins_data_1H

SUPPORTED_CURRENCY = 'usd'


def execute_coin_stream_1M(event, context):
    assets = get_coins_data(SUPPORTED_CURRENCY)
    assets = filter_coins_data(assets)
    print(assets)
    save_coins_data_live(assets)


def execute_coin_stream_1H(event, context):
    assets = get_coins_data(SUPPORTED_CURRENCY)
    assets = filter_coins_data(assets)
    print(assets)
    save_coins_data_1H(assets)


def execute_delete_old_5D():
    pass


def execute_delete_old_5Y():
    pass
