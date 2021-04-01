#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from datetime import time

import tconfig
from colors import b_colors
from customException import TickerSearchException
from tradingview import TradingView

"""
Utilities func
For validate requirements tickers format
"""

tradingView = TradingView()


def validate_format(ticker: str):
    valid_tickers_pattern = re.compile("[A-Z]+:[A-Z]+")
    if valid_tickers_pattern.match(ticker):
        print(b_colors.WARNING + 'VALID TICKER => ' + ticker + b_colors.ENDC)
        return True
    else:
        print(b_colors.WARNING + 'INVALID TICKER => ' + ticker + b_colors.ENDC)
        return False


def validate_tickers_list_id(list_id: int):
    for symbols_list in tradingView.symbols_list:
        if symbols_list.get_id() == list_id:
            return True
    else:
        return False


def repair_ticker_format(invalid_ticker: str):
    """
    Get invalid ticker.
    Return suggested valid ticker format.
    """

    if tconfig.exist(invalid_ticker):
        print(b_colors.OKGREEN + 'Ticker ' + invalid_ticker + ' found in config' + b_colors.ENDC)
        return tconfig.get_value(invalid_ticker)
    else:
        print(b_colors.OKCYAN + 'Ticker ' + invalid_ticker + ' getting request' + b_colors.ENDC)
        suggested_ticker = tradingView.ticker_search(invalid_ticker)
        time.sleep(0.5)
        if suggested_ticker:
            tconfig.write(invalid_ticker, suggested_ticker[0])
            return suggested_ticker[0]
        else:
            raise TickerSearchException(f'Warning: Something with ticker_search goes wrong!\n'
                                        f'suggested_ticker from ticker_search = 0')
