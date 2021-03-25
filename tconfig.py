#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from colors import b_colors

tickers_list: dict = {}


def load_from_file():
    global tickers_list
    try:
        with open('tconfig.json') as f:
            tickers_list = json.load(f)
    except IOError:
        print(b_colors.FAIL + "File tconfig not accessible! Please check file: tconfig.json" + b_colors.ENDC)
    finally:
        f.close()


def save():
    with open('tconfig.json', 'w') as f:
        json.dump(tickers_list, f, indent=2, sort_keys=True)


def exist(ticker: str):
    if ticker in tickers_list.keys():
        return True
    else:
        return False


def get_all():
    return tickers_list


def write(invalid_ticker_name: str, suggested_ticker: str):
    tickers_list[invalid_ticker_name] = suggested_ticker


def get_value(ticker: str):
    return tickers_list.get(ticker)
