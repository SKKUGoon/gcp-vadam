import geopandas as gpd
import pandas as pd
from datetime import datetime

def load_seoul_land(path: str):
    data = gpd.read_file(path + "/LSMD_CONT_LDREG_11_202411.shp")
    
    # Set CRS
    # data = data.set_crs(epsg=5186)
    data = data.to_crs(epsg=4326)

    data.columns = ["pnu", "jibun", "chk", "_oid", "sigungu_cd", "geometry"]
    data = data[["pnu", "jibun", "chk", "sigungu_cd", "geometry"]]
    
    return data
