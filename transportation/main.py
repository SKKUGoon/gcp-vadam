from dotenv import load_dotenv

import requests
from copy import deepcopy
import os

# "https://www.bigdata-transportation.kr/api?apiKey=a7867cc2-eee2-432f-b7ef-4b56c9c8a48e&productId=PRDTNUM_000000020308&tmType=1"


class TransportationDB:
    def __init__(self, envfile: str | None = ".env"):
        if envfile is not None:
            load_dotenv(envfile)

        self.base = "https://www.bigdata-transportation.kr/api"
        self.apikey = os.getenv("APIKEY_TDB")
        self.max_repeat = 10_000

    def korea_highway_tollgate_flow(self, verbose: bool = False):
        param = {
            "apiKey": self.apikey,
            "productId": "PRDTNUM_000000020308",
            "tmType": "1",  # 1 for 1 hour, 2 for 15 minute
        }
        
        resp = requests.get(self.base, params=param)
        if resp.status_code != 200:
            raise RuntimeError(resp.text)
        
        traffic = list()

        data = resp['result']
        traffic.append(data['trafficIc'])
        total_page = int(data['pageSize'])
        curr_page = int(data['pageNo'])
        
        while total_page >= curr_page:

            curr_page += 1
            ...
        
        ...
