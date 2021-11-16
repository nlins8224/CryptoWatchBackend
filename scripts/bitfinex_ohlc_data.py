from datetime import datetime
from time import mktime, sleep, time

from bfxapi import Client
from envyaml import EnvYAML

from config import init_database
from get_supported_coins import get_supported_coins_ids, get_supported_coins_sym

env = EnvYAML('env.yaml')

API_KEY = env['env_variables']['API_KEY']
API_SECRET = env['env_variables']['API_SECRET']

bfx = Client(
    API_KEY=API_KEY,
    API_SECRET=API_SECRET
)

SUPPORTED_COINS = '/supported-bitfinex'

MS_IN_SECOND = 1000
API_REQUESTS_PER_MINUTE_LIMIT = 90
SLEEP_TIME = (API_REQUESTS_PER_MINUTE_LIMIT / 60) + 0.25

_TIMEFRAMES = {
    '1h': 3600,
    '1m': 60,
    '1D': 3600 * 24
}
_TIMEFRAME = '1D'
_limit = 9999
_section = 'hist'

now_ms = round(time() * MS_IN_SECOND)

time_start_date = datetime(2015, 10, 10, 0, 0)
time_start_date_ms = mktime(time_start_date.timetuple()) * 1000

time_end_date = datetime(2021, 11, 15)
time_end_date_ms = mktime(time_end_date.timetuple()) * 1000

init_database()


async def get_historical_coin_data(coin, start, end, section, interval, limit, sort):
    response = await bfx.rest.get_public_candles(coin, start, end, section, interval, limit, sort)
    print(response)
    return response


async def get_historical_coins_data(start_ms, end_ms, section, interval, limit, sort):
    supported_coins_ids = get_supported_coins_ids(SUPPORTED_COINS)
    supported_coins_sym = get_supported_coins_sym(SUPPORTED_COINS)
    supported_coins_map = dict(zip(supported_coins_ids, supported_coins_sym))
    ms_in_interval = _TIMEFRAMES[interval] * MS_IN_SECOND

    data = dict()

    for coin in supported_coins_ids:
        coin_data = []
        step_start_ms = start_ms
        step_end_ms = end_ms
        step_ms = ms_in_interval * limit
        total_records = (step_end_ms - step_start_ms) / ms_in_interval
        while total_records > 0:
            if total_records < limit:
                step_ms = total_records * ms_in_interval
            step_end_ms = step_start_ms + step_ms
            coin_data += await get_historical_coin_data(coin, step_start_ms, step_end_ms, section, interval, limit,
                                                        sort)
            step_start_ms = step_start_ms + step_ms
            total_records -= limit
            sleep(SLEEP_TIME)

        coin_symbol = supported_coins_map[coin]
        data[coin_symbol] = coin_data

    return data
