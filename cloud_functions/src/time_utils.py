from datetime import datetime, timedelta
from time import time


def date_to_millis_UTC(date):
    utc_time = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    millis = (utc_time - datetime(1970, 1, 1)) // timedelta(milliseconds=1)
    return millis


def get_current_timestamp_ms():
    MS_IN_SECONDS = 1000
    return round(time() * MS_IN_SECONDS)


def trim_timestamp_to_midnight(timestamp):
    MS_IN_DAY = 24 * 60 * 60 * 1000
    return timestamp - (timestamp % MS_IN_DAY)


def get_n_days_ago_s(days_ago):
    date = datetime.now().replace(microsecond=0) - timedelta(days=days_ago)
    return int(date.timestamp())
