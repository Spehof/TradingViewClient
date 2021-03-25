#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from colors import b_colors

"""
Utilities func
For validate requirements tickers format
"""


def validate_format(ticker: list):
    valid_tickers_pattern = re.compile("[A-Z]+:[A-Z]+")
    if valid_tickers_pattern.match(ticker):
        print(b_colors.WARNING + 'VALID TICKER => ' + ticker + b_colors.ENDC)
        return True
    else:
        print(b_colors.WARNING + 'INVALID TICKER => ' + ticker + b_colors.ENDC)
        return False
