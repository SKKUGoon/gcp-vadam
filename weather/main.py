from abc import ABC
from dotenv import load_dotenv
from os import getenv
from datetime import datetime

import requests
import pandas as pd

from database.access import SDA


class WeatherAPI(ABC):
    def __init__(self, envfile: str | None = ".env") -> None:
        if envfile is not None:
            load_dotenv(envfile)
        pass


class KoreaWeather(WeatherAPI):
    def __init__(self) -> None:
        super().__init__()
        
        envkey = "APIKEY_KOREA_WEATHER"
        self.url = "https://apihub.kma.go.kr/api/typ01/url/"
        self.apikey = getenv(envkey)

    def get_station_information(self, date: datetime):
        endpoint = "stn_inf.php"
        param = {
            "inf": "SFC",  # SFC(지상), AWS(AWS)
            "tm": date.strftime("%Y%m%d%H%M"),
            "stn": 0,
            "help": 0,
            "authKey": self.apikey
        }

        resp = requests.get(self.url + endpoint, params=param)
        if resp.status_code != 200:
            raise RuntimeError(resp.text)
        
        column_names = [
            "stn_id", "lng", "lat", "stn_cd1", 
            "ht", "ht_pa", "ht_ta", "st_wd", "st_rn", 
            "stn_cd2", "stn_nm_kor", "stn_nm_eng", "fct_cd", "pnu_bjd", "-"
        ]
        float_columns = ["lng", "lat", "ht", "ht_pa", "ht_ta", "st_wd", "st_rn"]
        stations = self.parser(resp.text, column_names)[[c for c in column_names  if c != "-"]]
        stations[float_columns] = stations[float_columns].map(float)

        return stations

    def get_temperature_time(self, date: datetime):
        endpoint = "kma_sfctm2.php"
        param = {
            "tm": date.strftime("%Y%m%d%H%M"),
            "stn": 0,
            "help": 1,
            "authKey": self.apikey
        }

        resp = requests.get(self.url + endpoint, params=param)
        if resp.status_code != 200:
            raise RuntimeError(resp.text)
        
        column_names = [
            "datetime_str", "stn_id", "wind_direction", "wind_speed", 
            "gust_direction", "gust_speed", "gust_time", 
            "ground_hpa", "sealevel_hpa", "_pt", "_pr",
            "temperature", "_td", "humidity", "_pv", 
            "rain", "rain_day1", "rain_day2", "rain_strength",
            "snow_3hours", "snow_day", "snow_cumul", 
            "_wc", "_wp", "weather_report", 
            "cloud_total", "cloud_mid_ht", "cloud_min_ht",
            "cloud_type", "_ct_top", "_ct_mid", "_ct_low", 
            "visibility", "sun", "_si", 
            "status_ground", "temperature_ground", "_te005", "_te010", "_te020", "_te030",
            "status_sealevel", "wave", "_bf", "is_raining", "_ix",
        ]
        float_columns = [
            "wind_direction", "wind_speed", "gust_direction", "gust_speed",
            "ground_hpa", "sealevel_hpa", "temperature", "humidity", "rain", 
            "rain_day1", "rain_day2", "rain_strength", "snow_3hours", "snow_day", 
            "snow_cumul", "cloud_total", "cloud_mid_ht", "cloud_min_ht", 
            "visibility", "temperature_ground", "wave",
        ]
        basic_weather = self.parser(resp.text, column_names)[[c for c in column_names if not c.startswith("_")]]
        basic_weather[float_columns] = basic_weather[float_columns].map(float)

        return basic_weather

    def get_temperature_date(self, date: datetime):
        endpoint = "kma_sfctm2.php"
        param = {
            "tm": date.strftime("%Y%m%d%H%M"),
            "stn": 0,
            "help": 1,
            "authKey": self.apikey
        }
        print(self.url + endpoint, param)
        resp = requests.get(self.url + endpoint, params=param)
        if resp.status_code != 200:
            raise RuntimeError(resp.text)
        
        column_names = [
            "datetime_str", "stn_id", "wind_direction", "wind_speed", 
            "gust_direction", "gust_speed", "gust_time", 
            "ground_hpa", "sealevel_hpa", "_pt", "_pr",
            "temperature", "_td", "humidity", "_pv", 
            "rain", "rain_day1", "rain_day2", "rain_strength",
            "snow_3hours", "snow_day", "snow_cumul", 
            "_wc", "_wp", "weather_report", 
            "cloud_total", "cloud_mid_ht", "cloud_min_ht",
            "cloud_type", "_ct_top", "_ct_mid", "_ct_low", 
            "visibility", "sun", "_si", 
            "status_ground", "temperature_ground", "_te005", "_te010", "_te020", "_te030",
            "status_sealevel", "wave", "_bf", "is_raining", "_ix",
        ]
        float_columns = [
            "wind_direction", "wind_speed", "gust_direction", "gust_speed",
            "ground_hpa", "sealevel_hpa", "temperature", "humidity", "rain", 
            "rain_day1", "rain_day2", "rain_strength", "snow_3hours", "snow_day", 
            "snow_cumul", "cloud_total", "cloud_mid_ht", "cloud_min_ht", 
            "visibility", "temperature_ground", "wave",
        ]
        basic_weather = self.parser(resp.text, column_names)[[c for c in column_names if not c.startswith("_")]]
        basic_weather[float_columns] = basic_weather[float_columns].map(float)

        return basic_weather

    @staticmethod
    def parser(text: str, column_names):
        start_token, end_token = "#START7777", "#7777END"
        
        start_index = text.find(start_token)
        end_index = text.find(end_token, start_index)
        if start_index == -1 or end_index == -1:
            raise ValueError("cannot find start token or end token")

        # Extract the data block
        data_block = text[start_index + len(start_token):end_index]
        
        lines = data_block.strip().split("\n")
        lines = [line for line in lines if line.strip() != '']  # Remove empty lines
        
        data_lines = [
            [l for l in line.split(' ') if l != ''] 
            for line in lines if not line.strip().startswith('#')
        ]
        data_lines = [l for l in data_lines if len(l) == len(column_names)]
        
        return pd.DataFrame(data_lines, columns=column_names)

    def run(self, date: datetime | None = None, test: bool = False):
        if date is None:
            date = datetime.now()

        # Update station information
        stations = self.get_station_information(date)
        stations['updated_date'] = [date] * len(stations)
        stations['is_deleted'] = [False] * len(stations)

        db = SDA()
        df = db.select_sql_dataframe("select * from nimbus.station", verbose=False)
        
        new_id = [id for id in stations['stn_id'] if id not in df['stn_id'].tolist()]
        _dep_id = [id for id in df['stn_id'] if id not in stations['stn_id'].tolist()]  # Update is_deleted later

        stations_insertible = stations.loc[stations['stn_id'].isin(new_id)]
        if not test and len(stations_insertible) > 0:
            db.insert_dataframe(stations_insertible, "station", "nimbus")

        # Insert Weather information (Time)
        # Insert Weather information (Day)
        basic_weather = self.get_temperature_time(date)
        # basic_weather['datetime_str'] = basic_weather['datetime_str'].apply(lambda x: x[:8])

        print(basic_weather)
        basic_weather = basic_weather.loc[basic_weather['stn_id'].isin(stations['stn_id'])]
        if not test and len(basic_weather) > 0:
            db.insert_dataframe(basic_weather, "measurements_time", "nimbus")

        return


class USAWeather(WeatherAPI):
    def __init__(self) -> None:
        super().__init__()

    def get_temperature(self):
        raise NotImplementedError()
    
    def run(self):
        raise NotImplementedError()
    

class JapanWeather(WeatherAPI):
    def __init__(self) -> None:
        super().__init__()

    def get_temperature(self):
        raise NotImplementedError()
    
    def run(self):
        raise NotImplementedError()
