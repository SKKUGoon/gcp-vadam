import pandas as pd

from datetime import datetime, timedelta
from database.korea_investment import KISAuth


def generate_full_calendar(s: datetime, e: datetime):
    # s and e should be
    ptr = s
    row = list()

    while ptr.strftime("%Y%m%d") <= e.strftime("%Y%m%d"):
        is_last_day = False
        is_first_day = False

        if (ptr + timedelta(days=1)).month != ptr.month:
            # Last date of the month
            is_last_day = True
        if ptr.day == 1:
            is_first_day = True

        d = [
            ptr.year,
            ptr.month,
            ptr.day,
            ptr.strftime("%Y%m%d"),
            ptr.weekday(),
            is_first_day,
            is_last_day
        ]
        row.append(d)
        ptr += timedelta(days=1)

    return pd.DataFrame(row, columns=["year", "month", "day", "date_str", "weekday", "month_first_day", "month_last_day"])


def exchange_calendar_response(date_dict: dict):
    bzdy = False
    tr = False
    opened = False
    settle = False

    if date_dict['bzdy_yn'] == "Y":
        bzdy = True

    if date_dict['tr_day_yn'] == "Y":
        tr = True

    if date_dict['opnd_yn'] == "Y":
        opened = True

    if date_dict['sttl_day_yn'] == "Y":
        settle = True

    return [date_dict['bass_dt'], bzdy, tr, opened, settle]  # bass_dt is key


def generate_available_dates(s: datetime, e: datetime):
    kis = KISAuth()
    kis.get_oauth()

    # s and e should be
    ptr = s
    row = list()

    while ptr.strftime("%Y%m%d") <= e.strftime("%Y%m%d"):
        data, head = kis.get_holiday(ptr.strftime("%Y%m%d"))
        # Insert next key
        ptr = datetime.strptime(data['ctx_area_nk'].strip(), "%Y%m%d")
        data = list(map(exchange_calendar_response, data['output']))

        row += data

    kis.drop_oauth()
    return pd.DataFrame(row, columns=['date_str', 'business_day', 'trade_day', 'exchange_opened_day', 'settle_day'])
