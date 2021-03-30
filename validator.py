#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from colors import b_colors
from tradingview import TradingView

"""
Utilities func
For validate requirements tickers format
"""

tradingView = TradingView()


def validate_format(ticker: list):
    valid_tickers_pattern = re.compile("[A-Z]+:[A-Z]+")
    if valid_tickers_pattern.match(ticker):
        print(b_colors.WARNING + 'VALID TICKER => ' + ticker + b_colors.ENDC)
        return True
    else:
        print(b_colors.WARNING + 'INVALID TICKER => ' + ticker + b_colors.ENDC)
        return False


def validate_tickerslist_id(list_id: int):
    for symbols_list in tradingView.symbols_list:
        if symbols_list.get_id() == list_id:
            return True
        else:
            return False
