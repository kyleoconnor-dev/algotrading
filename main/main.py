"""
file: main.py
description: main algorithmic trading script
created by: Kyle O'Connor
created: 2021-05-03
last modified: 2021-05-03
"""

import inspect
import os
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
    with open(stock_sym_loc, 'r') as f:
        for line in f.readlines():
            sym = line.strip().split('\t')[0]
            try:
                data = si.get_data(sym)
                # get 13 and 48.5 day moving average
                x=1
            except AssertionError:
                print('No data found')

if __name__ == '__main__':
    main()
