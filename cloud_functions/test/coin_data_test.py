from cloud_functions.test.open_coins_data import open_coins_data
from cloud_functions.src.coins_data import parse_coins_data


def parse_coins_data_test():
    data = open_coins_data('resources/coins_data.json')
    parsed_entry = open_coins_data('resources/parsed_coins_data.json')

    data = parse_coins_data(data)
    entry = data[0].__dict__

    assert entry == parsed_entry
    assert data is not None
