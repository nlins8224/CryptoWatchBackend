from coins_data import get_coins_data, parse_coins_data, save_coins_data, save_coins_data_latest, delete_old_coins_data, \
    parse_coins_data_minimum
from coins_historical_data import historical_coins_data
from config import init_database
from supported_coins import save_supported_coins
from time_utils import trim_timestamp_to_midnight, get_current_timestamp_ms, get_n_days_ago_s

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

SUPPORTED_CURRENCY = 'usd'
LIVE_COINS = '/live-coins'
HISTORICAL_COINS_1D_PATH = '/historical-coins-1D'
HISTORICAL_COINS_1M_PATH = '/historical-coins-1M'
HISTORICAL_COINS_1M_5D_FILTERED_PATH = '/historical-coins-1M-5D-filtered'

CUT_OFF_TIME_5D_AGO = 5 * 24 * 60 * 60 * 1000
CUT_OFF_TIME_5Y_AGO = 5 * 365 * 24 * 60 * 60 * 1000

MS_IN_SECOND = 1000
CURRENT_TIMESTAMP = get_current_timestamp_ms()
# GMT 2015-01-01 00:00:00
START_S_5Y_AGO = 1420070400
START_S_5D_AGO = get_n_days_ago_s(5)
END_S = trim_timestamp_to_midnight(CURRENT_TIMESTAMP) // MS_IN_SECOND
init_database()


def execute_coin_batch_1M(event, context):
    assets = get_coins_data(SUPPORTED_CURRENCY)
    assets = parse_coins_data(assets)
    save_coins_data_latest(assets, LIVE_COINS)
    save_coins_data(assets, HISTORICAL_COINS_1M_PATH)


def execute_coin_batch_1D(event, context):
    assets = get_coins_data(SUPPORTED_CURRENCY)
    assets = parse_coins_data(assets)
    save_coins_data(assets, HISTORICAL_COINS_1D_PATH)


def execute_coin_batch_1M_5D_filtered(event, context):
    assets = get_coins_data(SUPPORTED_CURRENCY)
    assets = parse_coins_data_minimum(assets)
    save_coins_data(assets, HISTORICAL_COINS_1M_5D_FILTERED_PATH)


def execute_coin_historical_batch_1D(event, context):
    historical_coins_data(SUPPORTED_CURRENCY, HISTORICAL_COINS_1D_PATH, START_S_5Y_AGO, END_S)


def execute_coin_historical_1M_5D_filtered_batch(event, context):
    historical_coins_data(SUPPORTED_CURRENCY, HISTORICAL_COINS_1M_5D_FILTERED_PATH, START_S_5D_AGO,
                          CURRENT_TIMESTAMP // MS_IN_SECOND)


def execute_delete_old_coins_data_5D(event, context):
    delete_old_coins_data(HISTORICAL_COINS_1M_PATH, CUT_OFF_TIME_5D_AGO)


def execute_delete_old_coins_data_5D_filtered(event, context):
    delete_old_coins_data(HISTORICAL_COINS_1M_5D_FILTERED_PATH, CUT_OFF_TIME_5D_AGO)


def execute_delete_old_coins_data_5Y(event, context):
    delete_old_coins_data(HISTORICAL_COINS_1D_PATH, CUT_OFF_TIME_5Y_AGO)


def execute_save_supported_coins_coingecko(event, context):
    save_supported_coins(coins)
