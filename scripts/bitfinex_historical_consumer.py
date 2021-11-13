import asyncio
import datetime
import time

import pandas as pd
from bfxapi import Client

bfx = Client(
    API_KEY='kq9H6OgvM5s4hHUdA4gwvbjgBQHaflXxD0uiziM2OuO',
    API_SECRET='c4VQP8ZTwzycUJZW3eeKPukv8IovpZ3mSHye1PnXjum'
)

_symbols = ['tETHUSD', 'tBTCUSD',
            'tEOSUSD', 'tXLMUSD',
            'tADAUSD', 'tXRPUSD',
            'tLTCUSD', 'tBCHUSD',
            'tDOTUSD', 'tXMRUSD',
            'tSOLUSD', 'tLTCUSD',
            'tEOSUSD', 'tIOTUSD',
            'tNEOUSD', 'tBNBUSD',
            'tXRPUSD', 'tDOGUSD',
            'tLUNAUSD', 'tUNIUSD',
            'tAVAXUSD', 'tLINKUSD',
            'tLTCUSD', 'tSHIBUSD',
            'tMATICUSD', 'tFILUSD',
            'tXLMUSD', 'tATOUSD',
            'tCROUSD', 'tEOSUSD',
            'tAAVEUSD', 'tTRXUSD',
            'tXMRUSD', 'tMIOTAUSD',
            'tXEMUSD']

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

time_start_date = datetime.datetime(2021, 10, 10, 0, 0)
time_start_date_ms = time.mktime(time_start_date.timetuple()) * 1000

time_end_date = datetime.date(2021, 10, 10)
time_end_date_ms = time.mktime(time_end_date.timetuple()) * 1000


async def get_symbol_historical(symbol, start, end, section, interval, limit, sort):
    response = await bfx.rest.get_public_candles(symbol, start, end, section, interval, limit, sort)
    print(response)
    return response


def convert_to_csv(source, symbol):
    names = ['Date', 'Open', 'Close', 'High', 'Low', 'Volume']
    df = pd.DataFrame(source, columns=names)
    df.drop_duplicates(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df.set_index('Date', inplace=True)
    df.to_csv(f"{time_start_date}_{time_end_date}_{symbol}_{_TIMEFRAME}.csv")


async def get_historical_data(symbols, start_ms, end_ms, section, interval, limit, sort):
    ms_in_interval = _TIMEFRAMES[interval] * MS_IN_SECOND

    for symbol in symbols:
        data = []
        step_start_ms = start_ms
        step_end_ms = end_ms
        step_ms = ms_in_interval * limit
        total_records = (step_end_ms - step_start_ms) / ms_in_interval
        while total_records > 0:
            if total_records < limit:
                step_ms = total_records * ms_in_interval
            step_end_ms = step_start_ms + step_ms
            data += await get_symbol_historical(symbol, step_start_ms, step_end_ms, section, interval, limit, sort)
            step_start_ms = step_start_ms + step_ms
            total_records -= limit
            time.sleep(SLEEP_TIME)

        if data:
            convert_to_csv(data, symbol)


loop = asyncio.get_event_loop()
result = loop.run_until_complete(get_historical_data(_symbols, time_start_date_ms, time_end_date_ms,
                                                     _section, _TIMEFRAME, _limit, 1))
