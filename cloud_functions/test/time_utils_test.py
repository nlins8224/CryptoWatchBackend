from datetime import datetime

from freezegun import freeze_time

import cloud_functions.src.time_utils as time_utils


def date_to_millis_UTC_test():
    date_1 = '2021-11-09T22:46:35.211Z'
    date_2 = '2021-11-09T22:46:35.0Z'
    timestamp_1 = 1636497995211
    timestamp_2 = 1636497995000

    millis_1 = time_utils.date_to_millis_UTC(date_1)
    millis_2 = time_utils.date_to_millis_UTC(date_2)

    assert millis_1 == timestamp_1
    assert millis_2 == timestamp_2


@freeze_time('2020-04-05')
def get_current_timestamp_ms_test():
    MS_IN_SECONDS = 1000
    now_ms = int(datetime.utcnow().timestamp() * MS_IN_SECONDS)

    timestamp = time_utils.get_current_timestamp_ms()

    assert timestamp == now_ms


@freeze_time('2020-04-05 12:00:01')
def trim_timestamp_to_midnight_test():
    MS_IN_SECONDS = 1000
    timestamp = int(datetime.utcnow().timestamp() * MS_IN_SECONDS)
    trimmed_timestamp = 1586044800000  # 2020-04-05 00:00:00

    timestamp = time_utils.trim_timestamp_to_midnight(timestamp)

    assert timestamp == trimmed_timestamp
