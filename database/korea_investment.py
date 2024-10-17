from dotenv import load_dotenv

import requests
import os
import json


class KISAuth:
    domain = "https://openapi.koreainvestment.com:9443"

    def __init__(self, envfile: str | None = ".env"):
        if envfile is not None:
            load_dotenv()
        self.appkey = os.getenv("APIKEY_KIS_APP_KEY")
        self.secret = os.getenv("APIKEY_KIS_SECRET_KEY")
        self.expire = os.getenv("APIKEY_KIS_EXPIRE_DATE")
        self.account = os.getenv("APIKEY_KIS_ACCOUNT_NUM")
        self.token: str | None = None

    def __repr__(self):
        return f"""
App Key: {self.appkey}\nApp Secret: {self.secret}\nToken: {self.token}
"""
    
    def get_oauth(self, verbose: bool = False):
        endpoint = "/oauth2/tokenP"
        resp = requests.post(f"{self.domain}{endpoint}",
                             json.dumps({
                                 "grant_type": "client_credentials",
                                 "appkey": self.appkey,
                                 "appsecret": self.secret,
                             }))
        response = resp.json()
        self.token = response["access_token"]

        if verbose:
            print("oauth token generated")

    def drop_oauth(self, verbose: bool = False):
        if self.token is None:
            print("no oauth token to drop")
            return
        endpoint = "/oauth2/revokeP"
        resp = requests.post(f"{self.domain}{endpoint}",
                             json.dumps({
                                 "appkey": self.appkey,
                                 "appsecret": self.secret,
                                 "token": self.token
                             }))
        response = resp.json()
        if str(response["code"]) != "200":
            print("failed to drop oauth token")
            return
        
        if verbose:
            print("oauth token dropped")

    def get_bearer_token(self):
        return f"Bearer {self.token}"

    def get_holiday(self, get_info_from: str):
        """
        :param get_info_from: %Y%m%d
        :return:
        """
        endpoint = "/uapi/domestic-stock/v1/quotations/chk-holiday"

        if self.token is None:
            print("no oauth token")
            return

        hdr = {
            "content-type": "application/json; charset=utf-8",
            "authorization": self.get_bearer_token(),
            "appkey": self.appkey,
            "appsecret": self.secret,
            "tr_id": "CTCA0903R",
            "custtype": "P",
        }
        qry = {
            "BASS_DT": get_info_from,
            "CTX_AREA_NK": "",
            "CTX_AREA_FK": "",
        }

        resp = requests.get(f"{self.domain}{endpoint}",
                            params=qry,
                            headers=hdr)
        response = resp.json()
        headers = resp.headers
        return response, headers