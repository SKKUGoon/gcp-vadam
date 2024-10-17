from datetime import datetime, timedelta


def nearest_fwd_weekday(query_date: datetime):
    if query_date.weekday() == 5:
        return query_date + timedelta(days=2)

    if query_date.weekday() == 6:
        return query_date + timedelta(days=1)
    return query_date
