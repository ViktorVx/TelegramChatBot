import datetime


def extract_date(tx_date):
    return datetime.date(int(tx_date[4:]) + 2000, int(tx_date[2:4]), int(tx_date[:2]))


def extract_time(tx_time):
    return datetime.time(int(tx_time[:2]), int(tx_time[2:]))
