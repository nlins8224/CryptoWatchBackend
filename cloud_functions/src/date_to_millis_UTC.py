from datetime import datetime, timedelta


def date_to_millis_UTC(date):
    utc_time = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    millis = (utc_time - datetime(1970, 1, 1)) // timedelta(milliseconds=1)
    return millis
