import pytz
from datetime import datetime
from database.access import SDA


def avail_date_check(dt: datetime | None = None):
    db = SDA()

    # All monthly jobs are daily jobs.
    # They will only run for one day - First trade day of the month
    # If it's not 'trade_day' - Return False
    if dt is None:
        KST = pytz.timezone('Asia/Seoul')
        now = datetime.now(KST)
        y, m = now.year, now.month
    else:
        y, m = dt.year, dt.month

    sql_base = "select year, month, day from nimbus.calendar"
    predicate = " and ".join([
        f"year = {y}",
        f"month = {m}",
        f"exchange_opened_day"
    ])
    oth = " ".join([
        "order by day asc",
        "limit 1"
    ])

    my_cal = db.select_sql_dataframe(f"{sql_base} where {predicate} {oth};")
    ymd = my_cal.to_numpy()
    if len(ymd) != 1:
        print(f"calendar error. {len(ymd)} rows retrieved from date_check")
        return False

    first_date = datetime(ymd[0][0], ymd[0][1], ymd[0][2])
    compare = datetime(dt.year, dt.month, dt.day)
    return first_date == compare


def avail_hist_ym_first_date(start_date: datetime, end_date: datetime):
    db = SDA()

    sd, ed = start_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d")

    sql_base = "select year, month, min(day) as day from nimbus.calendar"
    predicate = " and ".join([
        f"day_str >= '{sd}'",
        f"day_str <= '{ed}'",
        f"exchange_opened_day"
    ])
    oth = " ".join([
        "group by year, month",
        "order by year, month, day"
    ])

    my_cal = db.select_sql_dataframe(f"{sql_base} where {predicate} {oth};")
    if len(my_cal) > 0:
        return list(map(lambda x: datetime(x[0], x[1], x[2]), my_cal.to_numpy()))
    else:
        return []


if __name__ == "__main__":
    # print(avail_date_check(datetime(2022, 3, 2)))
    s = avail_hist_ym_first_date(
        datetime(2022, 1, 1),
        datetime(2022, 5, 1)
    )
    print(s)
