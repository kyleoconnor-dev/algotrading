"""
file: main.py
description: main algorithmic trading script
created by: Kyle O'Connor
created: 2021-05-03
last modified: 2021-05-03
"""

import datetime as dt
import inspect
import os
import pandas as pd
import sys
import yahoo_fin.stock_info as si

SCRIPT_PTH = os.path.realpath(inspect.stack()[0][1])
SCRIPT_LOC = os.path.dirname(SCRIPT_PTH)
PARENT_DIR = os.path.dirname(SCRIPT_LOC)
sys.path.insert(0, SCRIPT_PTH)
sys.path.insert(0, SCRIPT_LOC)
sys.path.insert(0, PARENT_DIR)

stock_sym_loc = os.path.join(PARENT_DIR, 'docs', 'NYSE.txt')

def main():
    start = dt.datetime.now()
    count = 0
    with open(stock_sym_loc, 'r') as f:
        for line in f.readlines():
            sym = line.strip().split('\t')[0]
            try:
                data = si.get_data(sym)
                count += 1
                # get 13 and 48.5 day moving average
                data['13_DAY_EMA'] = data['close'].ewm(span=13).mean()
                data['48_DAY_EMA'] = data['close'].ewm(span=48.5).mean()
                data['50_DAY_EMA'] = data['close'].ewm(span=48.5).mean()
                data['200_DAY_EMA'] = data['close'].ewm(span=48.5).mean()
                fig = data.plot(x='index', y=['13_DAY_EMA'])
            except AssertionError:
                print('No data found')
                count += 1
            except KeyError:
                print('Random Key Error - skip')
                count += 1
    end = dt.datetime.now()
    total = end - start
    print(total)

if __name__ == '__main__':
    main()
