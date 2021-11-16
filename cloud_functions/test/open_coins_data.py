import json


def open_coins_data(name):
    with open(name) as data:
        return json.load(data)
