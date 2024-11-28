import geopandas as gpd
import pandas as pd
from datetime import datetime


def load_hjd(path: str):
    data = gpd.read_file(path + "/행정구역.shp")
    data = data.set_crs(epsg=5179)
    data = data.to_crs(epsg=4326)
    data.columns = [c.lower() for c in data.columns]
    return data


def load_sec(path: str):
    data = gpd.read_file(path + "/집계구.shp")
    data = data.set_crs(epsg=5179)
    data = data.to_crs(epsg=4326)
    data.columns = [c.lower() for c in data.columns]
    return data


def long_foreigner(path: str, date: datetime):
    date_str = date.strftime("%Y%m%d")
    try: 
        data = pd.read_csv(path + f"/LONG_FOREIGNER_{date_str}.csv")
    except UnicodeDecodeError:
        data = pd.read_csv(path + f"/LONG_FOREIGNER_{date_str}.csv", encoding="euc-kr")

    data.columns = ["date_str", "hour", "hjd_code", "sec_code", "total_population", "chinese", "non_chinese"]
    data = data[["date_str", "hour", "sec_code", "total_population", "chinese", "non_chinese"]]

    # Clean data types
    data["hour"] = data["hour"].astype(int)
    data[["total_population", "chinese", "non_chinese"]] = data[["total_population", "chinese", "non_chinese"]].replace("*", 0)
    data[["total_population", "chinese", "non_chinese"]] = data[["total_population", "chinese", "non_chinese"]].astype(float)

    return data


def locals(path: str, date: datetime):
    date_str = date.strftime("%Y%m%d")
    try: 
        data = pd.read_csv(path + f"/LOCAL_PEOPLE_{date_str}.csv")
    except UnicodeDecodeError:
        data = pd.read_csv(path + f"/LOCAL_PEOPLE_{date_str}.csv", encoding="euc-kr")

    data.columns = [
        "date_str", "hour", "hjd_code", "sec_code", "total_population", 
        "male_00_09", "male_10_14", "male_15_19", "male_20_24", "male_25_29", 
        "male_30_34", "male_35_39", "male_40_44", "male_45_49", "male_50_54", 
        "male_55_59", "male_60_64", "male_65_69", "male_70_up", 
        "female_00_09", "female_10_14", "female_15_19", "female_20_24", "female_25_29", 
        "female_30_34", "female_35_39", "female_40_44", "female_45_49", "female_50_54", 
        "female_55_59", "female_60_64", "female_65_69", "female_70_up"
    ]

    # Clean data types
    cols = [c for c in data.columns if c.startswith("male") or c.startswith("female")] + ["total_population"]
    data = data[["date_str", "hour", "sec_code", *cols]]
    data[cols] = data[cols].replace("*", 0)
    data[cols] = data[cols].astype(float)

    return data
