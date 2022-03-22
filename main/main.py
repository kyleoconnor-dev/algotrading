"""
file: main.py
description: main algorithmic trading script
created by: Kyle O'Connor
created: 2021-05-03
last modified: 2021-05-03
"""
import inspect
import os
import pandas as pd
import sys

SCRIPT_PTH = os.path.realpath(inspect.stack()[0][1])
SCRIPT_LOC = os.path.dirname(SCRIPT_PTH)
PARENT_DIR = os.path.dirname(SCRIPT_LOC)
sys.path.insert(0, SCRIPT_PTH)
sys.path.insert(0, SCRIPT_LOC)
sys.path.insert(0, PARENT_DIR)
from utilities.trading_utl import *
api_keys_dir = os.path.join(PARENT_DIR, 'keys')
x=1

def main():

    # data location
    data_loc = os.path.join(PARENT_DIR, 'docs', 'NYSE.txt')

    # directory for vantage key
    vantage_keys = os.path.join(api_keys_dir, 'vantage_key.txt')
    with open(vantage_keys, 'r') as f:
        v_key = f.readline()

    # get vantage key
    with open(vantage_keys, 'r') as f:
        vantage_key = f.readline().strip().split()[0]

    vantage_api_conn = AlphaVantageAPI(v_key)
    syms, desc = vantage_api_conn.get_nyse_symbols(data_loc)

    data = {}

    for s in syms:
        l = vantage_api_conn.get_ema(s, period='13')
        sh = vantage_api_conn.get_ema(s, period='48')
        data[s] = {}
        data[s]['long_ema'] = l
        data[s]['short_ema'] = sh

if __name__ == '__main__':
    main()
