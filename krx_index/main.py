import pandas as pd

import sys
import requests
from datetime import datetime

from database.access import SDA
from database.web_crawl_utility import RateLimit
from krx_index.common import nearest_fwd_weekday


def wics(dt: datetime):
    # Energy
    # Material
    # Industrials
    # Consumer Discretionary
    # Consumer Staples
    # Health Care
    # Financials and Real Estate
    # Information Technology
    # Communication Services
    # Utilities
    url = "https://www.wiseindex.com/Index/GetIndexComponets"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
    sectors = ("G10", "G15", "G20", "G25", "G30", "G35", "G40", "G45", "G50", "G55")

    # WICS instead of GICS (bloomberg only)
    db = SDA()
    lim = RateLimit()

    result = list()

    for s in sectors:
        data = {
            "ceil_yn": 0,
            "dt": dt.strftime("%Y%m%d"),
            "sec_cd": s
        }

        response = requests.get(url, data=data, headers=headers)
        lim.tick()

        if response.status_code == 200:
            sector_info = response.json()
            stocks = map(lambda x: [x["CMP_CD"], x["SEC_NM_KOR"]], sector_info["list"])
            result.extend(stocks)
        else:
            raise FileNotFoundError("failed request")
    lim.reset()

    result = pd.DataFrame(result, columns=["stock_cd", "sector"])
    result["year"] = [dt.year] * len(result)
    result["month"] = [dt.month] * len(result)
    db.insert_dataframe(result, "wics", "nimbus")


def kospi200(dt: datetime):
    # Basic Request information
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    headers = {
        'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201050201',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    qd = nearest_fwd_weekday(dt)

    db = SDA()
    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT00601',
        'locale': 'ko_KR',
        'tboxindIdx_finder_equidx0_1': '코스피 200',
        'indIdx': '1',
        'indIdx2': '028',
        'codeNmindIdx_finder_equidx0_1': '코스피 200',
        'param1indIdx_finder_equidx0_1': '',
        'trdDd': qd.strftime("%Y%m%d"),
        'money': '3',
        'csvxls_isNo': 'false'
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        # Check if the request was successful
        if response.status_code == 200:
            # Print the response JSON
            data = response.json()
            data = data['output']
            data = list(map(lambda x: x['ISU_SRT_CD'], data))

            if len(data) <= 0:
                sys.exit(1)

            data = pd.DataFrame(data)
            data.columns = ["stock_cd"]
            data["year"] = [qd.year] * len(data)
            data["month"] = [qd.month] * len(data)
        else:
            raise FileNotFoundError("failed request")
        
        db.insert_dataframe(data, "krx_kospi200", "nimbus")
    except FileNotFoundError as e:
        print("Not the right date", e)


def kospi(dt: datetime):
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    headers = {
        'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201010101&idxIndMidclssCd=02&money=1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    qd = nearest_fwd_weekday(dt)
    
    db = SDA()
    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT00601',
        'locale': 'ko_KR',
        'tboxindIdx_finder_equidx0_1': '코스피',
        'indIdx': '1',
        'indIdx2': '001',
        'codeNmindIdx_finder_equidx0_1': '코스피',
        'param1indIdx_finder_equidx0_1': '',
        'trdDd': qd.strftime("%Y%m%d"),
        'money': '3',
        'csvxls_isNo': 'false'
    }

    try:
        response = requests.post(url, headers=headers, data=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Print the response JSON
            data = response.json()
            data = data['output']
            data = list(map(lambda x: x['ISU_SRT_CD'], data))

            if len(data) <= 0:
                sys.exit(1)

            data = pd.DataFrame(data)
            data.columns = ["stock_cd"]
            data["year"] = [qd.year] * len(data)
            data["month"] = [qd.month] * len(data)
        else:
            raise FileNotFoundError("failed request")
        
        db.insert_dataframe(data, "krx_kospi", "universe")
    except FileNotFoundError as e:
        print("Not the right date", e)
