from datetime import datetime
from weather.main import KoreaWeather
from database.access import SDA
import pytz
import pandas as pd


def insert_weather_history(db: SDA, start_date: datetime, end_date: datetime):
    sdt = start_date.replace(hour=0, minute=0, second=0)
    edt = end_date.replace(hour=23, minute=59, second=59)

    kw = KoreaWeather()

    date_range = pd.date_range(start=sdt, end=edt, freq='30D')
    
    for current_date in date_range:
        print(current_date, "~", min(current_date + pd.Timedelta(days=29, hours=23, minutes=59, seconds=59), edt))
        d = kw.get_temperature_time_period(
            current_date, 
            min(current_date + pd.Timedelta(days=29, hours=23, minutes=59, seconds=59), edt)
        )
        db.insert_dataframe(d, "station_measure_time", "nimbus")
    
