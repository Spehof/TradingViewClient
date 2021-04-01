#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

from requests.exceptions import InvalidURL

import tconfig
from colors import b_colors
import time
from cookieLoader import get_cookie
from customException import TickersListNotExist
from symbolsList import SymbolsList


class TradingView:
    """
    class for represents a client TV
    get/set/update/delete tickers across HTTP  backend server requests
    """

    def __init__(self):
        # TODO tickers list repair in subclass
        # TODO tickers search in subclass
        self.url_all_tickers_list: str = 'https://www.tradingview.com/api/v1/symbols_list/all/'
        self.url_curr_tickers: str = 'https://ru.tradingview.com/api/v1/symbols_list/active/'
        self.url_adding: str = 'https://www.tradingview.com/api/v1/symbols_list/colored/red/append/'
        # self.url_adding: str = 'https://ru.tradingview.com/api/v1/symbols_list/custom/19681992/append/'
        self.url_deleting: str = 'https://www.tradingview.com/api/v1/symbols_list/colored/red/remove/'
        # self.url_deleting: str = 'https://ru.tradingview.com/api/v1/symbols_list/custom/19681992/remove/'
        self.cookies_for_search: dict = {'cookie': get_cookie()}
        self.headers_for_search: dict = {
            'accept': '*/*',
            'x-language': 'en',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
        }
        self.headers: dict = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Cookie": get_cookie(),
            "DNT": "1",
            "Host": "ru.tradingview.com",
            "Origin": "https://ru.tradingview.com",
            "Referer": "https://ru.tradingview.com/chart/wfLFyqcn/",
            "TE": "Trailers",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0",
            "content-type": "application/json",
            "x-language": "ru",
            "x-requested-with": "XMLHttpRequest"
        }
        self.symbols_list: list = self.__init_symbols_lists()

    #     TODO write ticker_searcher subclass

    def __init_symbols_lists(self):
        symbols_list_filled: list = []
        symbols_list = requests.get(self.url_all_tickers_list, headers=self.headers).json()
        for symbol_list in symbols_list:
            symbols_list_filled.append(SymbolsList(symbol_list['id']))
        return symbols_list_filled

    def get_symbols_list(self, name: str) -> SymbolsList:
        if self.symbols_list.get(name):
            list = self.symbols_list.get(name)
        else:
            raise TickersListNotExist("Tickers list not found! NAME: " + name)
        return list

    def get_symbols_list(self, list_id: int) -> SymbolsList:
        for curr_symbol_list in self.symbols_list:
            if curr_symbol_list.get_id() == list_id:
                return curr_symbol_list
        else:
            raise TickersListNotExist("Tickers list not found! ID: " + str(list_id))

    def get_symbols_list_name(self, list_id: int) -> str:
        for symbols_list in self.symbols_list:
            if symbols_list.get_id() == list_id:
                return symbols_list.get_name()
            else:
                raise TickersListNotExist("Tickers list not found! ID: " + str(list_id))

    def get_symbols(self, list_id: int) -> list:
        return self.get_symbols_list(list_id).get_tickers()

    def add_tickers(self, list_id: int, tickers: list):
        self.get_symbols_list(list_id).add_tickers(tickers)

    def del_tickers(self, list_id: int, tickers: list):
        self.get_symbols_list(list_id).delete_tickers(tickers)

    def ticker_search(self, ticker: str):
        """
        ticker - ticker in string format for search
        return - list suggestion  in format - exchange:symbol
        """

        url_search = f'https://symbol-search.tradingview.com/symbol_search/?text={ticker}&hl=1&exchange=&lang=ru&type=&domain=production'
        suggestion_tickers = requests.get(url_search, headers=self.headers_for_search, cookies=self.cookies_for_search,
                                          timeout=5)
        if suggestion_tickers.status_code == 200:
            tickers_dict: dict = json.loads(suggestion_tickers.text)
            tickers_resp = []
            for ticker_dict in tickers_dict:
                symbol = ticker_dict['symbol'].replace(u'<em>', u'').replace(u'</em>', u'')
                tickers_resp.append(ticker_dict['exchange'] + ":" + symbol)
            return tickers_resp
        else:
            return []

    def free_all_tickers(self, list_id: int):
        """
        Delete all tickers from account.
        """

        ansver: str = input(
            b_colors.WARNING + "Are you sure, you want delete all you current tickers? Do you make backup? Y/n: " + b_colors.ENDC)
        if ansver == 'Y':
            print(b_colors.OKGREEN + "Deleting shares from list " + self.get_symbols_list_name(
                list_id) + "..." + b_colors.ENDC)
            self.del_tickers(list_id, self.get_symbols(list_id))
            print(b_colors.OKGREEN + "All pass good! You dashboard cleaned." + b_colors.ENDC)
        if ansver == 'n':
            print(b_colors.FAIL + "Deleting interrupted!" + b_colors.ENDC)

    def restore_tickers_list(self, tickers: list, invalid_tickers: list):
        """
        Restoring tickers list after validate.
        """

        if invalid_tickers:
            for invalid_ticker in invalid_tickers:
                tickers.remove(invalid_ticker)
                tickers.append(self.repair_ticker_format(invalid_ticker))
            return tickers
        else:
            print('No one invalid tickers found')
            return tickers

    def ping(self):
        # TODO: write getting account name
        pass
