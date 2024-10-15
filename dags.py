from airflow.decorators import task, dag
from datetime import datetime
import pytz


@dag(description="test1",
     start_date=datetime(2024, 10, 16, 9, 0, 0, tzinfo=pytz.timezone('Asia/Seoul')),
     tags=["test", "test1"],
     catchup=False)
def korean_weather():
    ...


@dag(description="test2",
     start_date=datetime(2024, 10, 16, 10, 0, 0, tzinfo=pytz.timezone('Asia/Seoul')),
     tags=["test", "test2"],
     catchup=False)
def korean_weather():
    ...
