from datetime import datetime

from freezegun import freeze_time

from time_utils import date_to_millis_UTC, get_current_timestamp_ms, trim_timestamp_to_midnight


def date_to_millis_UTC_test():
    date_1 = '2021-11-09T22:46:35.211Z'
    date_2 = '2021-11-09T22:46:35.0Z'
    timestamp_1 = 1636497995211
    timestamp_2 = 1636497995000

    millis_1 = date_to_millis_UTC(date_1)
    millis_2 = date_to_millis_UTC(date_2)

    assert millis_1 == timestamp_1
    assert millis_2 == timestamp_2


@freeze_time('2020-04-05')
def get_current_timestamp_ms_test():
    MS_IN_SECONDS = 1000
    now_ms = int(datetime.utcnow().timestamp() * MS_IN_SECONDS)

    timestamp = get_current_timestamp_ms()

    assert timestamp == now_ms


@freeze_time('2020-04-05 12:00:01')
def trim_timestamp_to_midnight_test():
    MS_IN_SECONDS = 1000
    timestamp = int(datetime.utcnow().timestamp() * MS_IN_SECONDS)
    trimmed_timestamp = 1586044800000  # 2020-04-05 00:00:00

    timestamp = trim_timestamp_to_midnight(timestamp)

    assert timestamp == trimmed_timestamp
