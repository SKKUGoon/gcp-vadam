from prefect import flow, task
from krx_index.main import kospi, kospi200, wics
from database.datetime_utility import avail_date_check
from datetime import datetime, timedelta
import pytz


@flow(name="monthly stock index component update", log_prints=True)
def update_krx_index():
    KST = pytz.timezone('Asia/Seoul')
    dt = datetime.now(KST)

    proceed = check_if_date_available(dt)

    if proceed:
        wrap_kospi(dt)  # to nimbus.kospi
        wrap_kospi200(dt)  # to nimbus.kospi200
        wics(dt - timedelta(days=1))


@task
def check_if_date_available(dt) -> bool:
    return avail_date_check(dt)


@task
def wrap_kospi(dt: datetime):
    kospi(dt)


@task
def wrap_kospi200(dt: datetime):
    kospi200(dt)


@task
def wrap_wics(dt: datetime):
    wics(dt)


if __name__ == "__main__":
    update_krx_index().from_source(
        source="https://github.com/SKKUGoon/gcp-vadam.git",
        entrypoint="krx_index/krx_etl.py:update_krx_index"
    ).deploy(
        name='krx-index',
        work_pool_name='data-etl',
    )
