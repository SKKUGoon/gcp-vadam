from prefect import flow, task
from weather.main import KoreaWeather
from datetime import datetime
import pytz


@flow(name="daily weather update", log_prints=True)
def update_weather() -> str:
    KST = pytz.timezone('Asia/Seoul')
    dt = datetime.now(KST)

    # Start Each Task
    korea_weather(dt)
    

@task
def korea_weather(dt: datetime):
    kw = KoreaWeather()
    kw.run(dt)


if __name__ == "__main__":
    update_weather().deploy(
        name='weather',
        work_pool_name='weather-work-pool',
        work_queue_name='weather-queue'
    )
