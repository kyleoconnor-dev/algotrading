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
import numpy as np
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
UNVERVALUED_SYM = list(UNDERVALUED_CAPS['Symbol'])

start = dt.datetime.now()

def get_ema(dataframe):

    dataframe['13_DAY_EMA'] = dataframe['close'].ewm(span=13).mean()
    dataframe['48_DAY_EMA'] = dataframe['close'].ewm(span=48.5).mean()
    dataframe['50_DAY_EMA'] = dataframe['close'].ewm(span=50).mean()
    dataframe['200_DAY_EMA'] = dataframe['close'].ewm(span=200).mean()

    return dataframe

def get_dip(data, today):
    prev_10_days = data.tail(10)
    ema_50 = np.array(prev_10_days['50_DAY_EMA'])
    gradient = np.gradient(ema_50)
    
    return gradient


def get_potential_stock_options():

    today = start.date()
    day_of_week = today.weekday()
    if day_of_week == 5:
        day_diff = 1
    elif day_of_week == 6:
        day_diff = 2
    else:
        day_diff = 0
    retrieve_start = today - dt.timedelta(days=365)
    retrieve_start = retrieve_start.strftime('%m/%d/%Y')
    count = 0
    stock_options = {}
    with open(stock_sym_loc, 'r') as f:
        for line in f.readlines():
            sym = line.strip().split('\t')[0]
            try:
                data = si.get_data(sym, index_as_date=False, start_date=retrieve_start)
                data['Date'] = data['date'].dt.date
                datapoint = list(data['Date'])[0]
                data = get_ema(data)
                today_data = data[data['Date'] == today - dt.timedelta(days=day_diff)]
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
                        print('No Stats')
                        stats_val = 'No stats valuation'
                    try:
                        company_info = si.get_company_info(sym)
                    except TypeError:
                        print('No company info')
                        company_info = "No Company Info"
                    pe_ratio = quote_table.get('PE Ratio (TTM)')

                    if pe_ratio < 20:
                        gradient = get_dip(data, today)
                        for va in gradient:
                            if va > -0.005 and va < 0.005:
                                # return stock options
                                stock_options[sym] = {}
                                stock_options[sym]['last_50_days_data'] = data.tail(50)
                                stock_options[sym]['company_info'] = company_info
                                stock_options[sym]['quote_data'] = quote_data
                                stock_options[sym]['quote_table'] = quote_table
                                stock_options[sym]['stats'] = stats
                                stock_options[sym]['stats_val'] = stats_val
                                x=1
                                break
                        count += 1
                    else:
                        count += 1
                        print(count)
                        continue
                else:
                    count += 1
                    print(count)
                    continue
            except AssertionError:
                print('No data found')
                count += 1
            except KeyError:
                print('Random Key Error - skip')
                count += 1
            print(count)
    return stock_options

def get_html(stock_options):
    pass

if __name__ == '__main__':
    stock_options = get_potential_stock_options()
