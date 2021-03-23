#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from tconfig import TconfigVrapper

# repair_ticker_format

tcw = TconfigVrapper()


class TickersValidator:
    """
    Utilities class
    For validate requirements tickers format
    """

    def validate_format(self, tickers: list):
        formatted_list = []
        valid_tickers_pattern = re.compile("[A-Z]+:[A-Z]+")
        for ticker in tickers:
            if not valid_tickers_pattern.findall(ticker):
                print('INVALID TICKER => ' + ticker)
                formatted_list.append(self.repair_format(ticker))
            else:
                formatted_list.append(ticker)
        return formatted_list
