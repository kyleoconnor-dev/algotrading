"""
file: main.py
description: main algorithmic trading script
created by: Kyle O'Connor
created: 2021-05-03
last modified: 2021-05-03
"""
import inspect
import os
import pathlib
import sys

SCRIPT_PTH = os.path.realpath(inspect.stack()[0][1])
SCRIPT_LOC = os.path.dirname(SCRIPT_PTH)
PARENT_DIR = os.path.dirname(SCRIPT_LOC)
sys.path.insert(0, SCRIPT_PTH)
sys.path.insert(0, SCRIPT_LOC)
sys.path.insert(0, PARENT_DIR)
from utilities.trading_utl import *
api_keys_dir = os.path.join(PARENT_DIR, 'keys')

def main():

    # directory for vantage key
    vantage_keys = os.path.join(api_keys_dir, 'vantage_key.txt')

    # get vantage key
    with open(vantage_keys, 'r') as f:
        vantage_key = f.readline().strip().split()[0]

    url_params = {
        'function': 'TIME_SERIES_INTRADAY', 'symbol': 'IBM',
        'interval': '5min', 'apikey': vantage_key
    }
    vantage_api_conn = AlphaVantageAPI(vantage_key)
    check = vantage_api_conn.get_time_series(url_params)
    

if __name__ == '__main__':
    main()
