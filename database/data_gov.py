from os import getenv

from dotenv import load_dotenv
import pandas as pd
import requests


from database.access import SDA


class DataGoKr:
    def __init__(self, envfile: str | None = ".env"):
        if envfile is not None:
            load_dotenv(envfile)

        self.apikey = getenv("APIKEY_DATA_GO_KR")
    
    