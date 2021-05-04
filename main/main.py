

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

    vantage_api_conn = AlphaVantageAPI(vantage_key)
    vantage_api_conn.auth = vantage_key
    




if __name__ == '__main__':
    main()
