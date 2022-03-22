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
        self.key = api_key
        self.endpoint = 'https://www.alphavantage.co/query?'

    @staticmethod
    def get_nyse_symbols(data_loc):

        stock_symbols = []
        stock_desc = {}
        with open(data_loc, 'r') as file:
            for line in enumerate(file.readlines()):
                if line[0] == 0:
                    pass
                else:
                    l = line[1].strip().split('\t')
                    if len(l) == 2:
                        sym = l[0]
                        desc = l[1]
                        stock_symbols.append(sym)
                        stock_desc[sym] = desc
                    elif len(l) == 1:
                        sym = l[0]
                        stock_symbols.append(sym)
                        stock_desc[sym] = 'No description'
                    else:
                        print('Not sure why this is blank')
                        pass

        return stock_symbols, stock_desc

    def get_ema(self, sym, period):

        url = f'{self.endpoint}function=EMA&symbol={sym}&interval=daily&' \
              f'time_period={period}&series_type=open&apikey={self.key}'
        response = requests.get(url)
        data = response.json()

        return data





        

