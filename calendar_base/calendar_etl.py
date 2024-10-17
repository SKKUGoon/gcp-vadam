import pandas as pd
from prefect import flow, task

from database.access import SDA
from calendar_base.main import generate_full_calendar, generate_available_dates

import pytz
from datetime import datetime, timedelta


@flow(name="monthly future calendar update", log_prints=True)
def update_calendar(month_ahead: int = 0):
    KST = pytz.timezone('Asia/Seoul')
    dt = datetime.now(KST)

    start_date = datetime(dt.year + 1 * (dt.month + month_ahead > 12),
                          (dt.month + month_ahead) % 12 + ((dt.month + month_ahead) % 12 == 0) * 12,
                          1,
                          0,
                          0,
                          0,
                          0,
                          KST)
    end_date = (start_date + timedelta(days=40)).replace(day=1) - timedelta(days=1)

    dts = wrap_gen_full_calendar(start_date, end_date)
    holi = wrap_gen_available_dates(start_date, end_date)
    holi = holi.drop_duplicates(subset=['day_str'])

    # Insert future calendar
    dt = pd.merge(dts, holi, how='left', on=['day_str'])
    insert_dataframe(dt)


@task
def wrap_gen_full_calendar(st: datetime, ed: datetime):
    return generate_full_calendar(st, ed)


@task 
def wrap_gen_available_dates(st: datetime, ed: datetime):
    return generate_available_dates(st, ed)


def insert_dataframe(dt: pd.DataFrame):
    db = SDA()
    db.insert_dataframe(dt, "calendar", "nimbus")


if __name__ == "__main__":
    update_calendar(4).deploy(
        name='calendar',
        work_pool_name='kis-work-pool',
        work_queue_name='calendar-queue'
    )

