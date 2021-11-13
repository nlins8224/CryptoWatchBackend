import json

from coins_data import filter_coins_data


def open_coins_data(name):
    with open(name) as data:
        return json.load(data)


def filter_market_data_test():
    data = open_coins_data('resources/coins_data.json')
    filtered_entry = open_coins_data('resources/filtered_coins_data.json')

    data = filter_coins_data(data)
    entry = data[0].__dict__

    assert entry == filtered_entry
    assert data is not None


filter_market_data_test()
