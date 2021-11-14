from pycoingecko import CoinGeckoAPI
from firebase_admin import db

cg = CoinGeckoAPI()
coins = ['bitcoin', 'dogecoin',
         'binancecoin', 'cardano',
         'ethereum', 'solana',
         'ripple', 'tether',
         'usd-coin', 'polkadot',
         'uniswap', 'chainlink',
         'litecoin', 'stellar',
         'cosmos', 'crypto-com-chain',
         'eos', 'tron',
         'monero', 'iota',
         'nem'
         ]


# Supported coins should be in form sym:id
def get_supported_coins():
    dict_pairs = dict()
    data = cg.get_coins_markets(vs_currency='usd', ids=coins)
    for entry in data:
        dict_pairs[entry['symbol']] = entry['id']

    return dict_pairs


def save_supported_coins(supported_coins):
    ref = db.reference('supported-coingecko')
    ref.set(supported_coins)
