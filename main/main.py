"""
file: main.py
description: main algorithmic trading script
created by: Kyle O'Connor
created: 2021-05-03
last modified: 2022-05-18
"""

import datetime as dt
import inspect
import os
import matplotlib.pyplot as plt
import pandas as pd
import sys
import yahoo_fin.stock_info as si
import warnings
warnings.filterwarnings("ignore")

SCRIPT_PTH = os.path.realpath(inspect.stack()[0][1])
SCRIPT_LOC = os.path.dirname(SCRIPT_PTH)
PARENT_DIR = os.path.dirname(SCRIPT_LOC)
sys.path.insert(0, SCRIPT_PTH)
sys.path.insert(0, SCRIPT_LOC)
sys.path.insert(0, PARENT_DIR)

stock_sym_loc = os.path.join(PARENT_DIR, 'docs', 'NYSE.txt')

SPANS = ['13', '48', '50', '200']

UNDERVALUED_CAPS = si.get_undervalued_large_caps()
x=1

def get_ema(dataframe):

    dataframe['13_DAY_EMA'] = dataframe['close'].ewm(span=13).mean()
    dataframe['48_DAY_EMA'] = dataframe['close'].ewm(span=48.5).mean()
    dataframe['50_DAY_EMA'] = dataframe['close'].ewm(span=50).mean()
    dataframe['200_DAY_EMA'] = dataframe['close'].ewm(span=200).mean()

    return dataframe

def main():
    start = dt.datetime.now()
    today = start.date()
    count = 0
    with open(stock_sym_loc, 'r') as f:
        for line in f.readlines():
            sym = line.strip().split('\t')[0]
            try:
                data = si.get_data(sym, index_as_date=False)
                data['Date'] = data['date'].dt.date
                datapoint = list(data['Date'])[0]
                data = get_ema(data)
                today_data = data[data['Date'] == today]
                values = [
                    list(today_data['13_DAY_EMA'])[0],
                    list(today_data['48_DAY_EMA'])[0],
                    list(today_data['50_DAY_EMA'])[0],
                    list(today_data['200_DAY_EMA'])[0]
                ]
                today_data_dict = {}
                for w, v in zip(SPANS, values):
                    today_data_dict[w] = v
                if today_data_dict['50'] < today_data_dict['200']:
                    quote_data = si.get_quote_data(sym)
                    quote_table = si.get_quote_table(sym)
                    stats = si.get_stats(sym)
                    try:
                        stats_val = si.get_stats_valuation(sym)
                    except IndexError:
                        print('No stats valuation')
                    try:
                        company_info = si.get_company_info(sym)
                    except TypeError:
                        print('No company info')
                    pe_ratio = quote_table.get('PE Ratio (TTM)')
                    if pe_ratio < 20:
                        data[['13_DAY_EMA', '50_DAY_EMA', '20_DAY_EMA']].plot()
                        plt.show()
                        x=1
                        count += 1
                    else:
                        count += 1
                else:
                    count += 1
                # add logic for making next steps
                # pseudo code
                # if 13_day < 48_day: bear market, do steps
                # else: bull market, skip 
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
