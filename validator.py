#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

"""
Utilities func
For validate requirements tickers format
"""


def validate_format(ticker: list):
    valid_tickers_pattern = re.compile("[A-Z]+:[A-Z]+")
    if valid_tickers_pattern.match(ticker):
        print('VALID TICKER => ' + ticker)
        return True
    else:
        print('INVALID TICKER => ' + ticker)
        return False
