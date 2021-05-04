"""
file: trading_utl.py
description: utilities for accessing API for algotrading
created by: Kyle O'Connor
created: 2021-05-02
last modified: 2021-05-02
"""

# imports
import datetime as dt
import json
import requests

class AlphaVantageAPI(requests.Session):

    def __init__(self, api_key):
        super(AlphaVantageAPI, self).__init__()
        self.endpoint = 'https://www.alphavantage.co/query?'

    def get_time_series(self, url_params):

        path = (
            f'{self.endpoint}{"&".join(f"{key}={value}" for key, value in url_params.items())}'
        )
        
        results = self.get(path)
        content = json.loads(results.content)

        return content


        

