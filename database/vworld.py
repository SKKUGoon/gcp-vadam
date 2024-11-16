import requests
from dotenv import load_dotenv
import os
from typing import Literal


class Vworld:
    def __init__(self):
        load_dotenv()
        self.apikey = os.getenv("APIKEY_VWORLD")
        self.base = "https://api.vworld.kr/req/address"
        pass

    def geocode_address_to_coord(self, address: str, address_type: Literal["parcel", "road"]):
        param = {
            "service": "address",
            "request": "getcoord",
            "version": "2.0",
            "crs": "epsg:4326",
            "address": address,
            "refine": "true",
            "simple": "false",
            "format": "json",
            "type": address_type,
            "key": self.apikey,
        }

        resp = requests.get(self.base, params=param)
        if resp.status_code != 200:
            raise RuntimeError("vworld request failed")
        
        data = resp.json()
        return data
