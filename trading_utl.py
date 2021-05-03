"""
file: trading_utl.py
description: utilities for accessing API for algotrading
created by: Kyle O'Connor
created: 2021-05-02
last modified: 2021-05-02
"""

# imports
import datetime as dt
import requests

class AlphaVantageAPI(requests.Session):

    def __init__(self, api_key):
        super(AlphaVantageAPI, self).__init__

        self.api_key = api_key
        self.endpoint = 'https://www.alphavantage.co/query?'

    def get_time_series(self)
        

