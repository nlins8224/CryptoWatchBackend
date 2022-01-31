import json

from cloud_functions.test.open_coins_data import open_coins_data
from cloud_functions.src.coins_historical_data import parse_historical_coin_data


def parse_historical_coin_data_test():
    coin_symbol = 'btc'
    data = open_coins_data('resources/coins_historical_data.json')
    parsed_data = open_coins_data('resources/parsed_coins_historical_data.json')

    data = parse_historical_coin_data(data, coin_symbol)

    assert json.dumps(data) == json.dumps(parsed_data)
