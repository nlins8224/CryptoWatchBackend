from pycoingecko import CoinGeckoAPI
import pandas as pd

cg = CoinGeckoAPI()
_coins = ['bitcoin', 'dogecoin',
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
_time = 'max'
coins = ['ripple']


def convert_to_csv(source, symbol):
    names = ['Date', 'Open', 'Close', 'High', 'Low']
    df = pd.DataFrame(source, columns=names)
    df.drop_duplicates(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df.set_index('Date', inplace=True)
    df.to_csv(f"{symbol}_{_time}.csv")


def get_ohlc_historical_data(coins, time):
    for coin in coins:
        ohlc = cg.get_coin_ohlc_by_id(coin, 'usd', time)
        convert_to_csv(ohlc, coin)


get_ohlc_historical_data(_coins, _time)
