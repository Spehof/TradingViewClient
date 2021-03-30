#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

from requests.exceptions import InvalidURL

import tconfig
from colors import b_colors
import time
from cookieLoader import get_cookie
from symbolsList import SymbolsList


class TradingView:
    """
    class for represents a client TV
    get/set/update/delete tickers across HTTP  backend server requests
    """

    def __init__(self):

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
        self.symbols_list: dict = self.__init_symbols_lists()
    #     TODO write ticker_searcher subclass

    def __init_symbols_lists(self):
        symbols_list_filled = {}
        symbols_list = requests.get(self.url_all_tickers_list, headers=self.headers).json()
        for symbol_list in symbols_list:
            symbols_list_filled.update({
                symbol_list['name']: SymbolsList(symbol_list['id'])
            })
        return symbols_list_filled

    def get_symbols_list(self, name: str):
        return self.symbols_list.get(name)

    def get_all_symbols_list_name(self):
        return self.symbols_list.keys()

    def get_all_symbol_list_id(self):
        lists_id = []
        for symbol_list_name in self.get_all_symbols_list_name():
            lists_id.append(self.symbols_list.get(symbol_list_name).get_id())
        return lists_id

    def get_symbols_in_list(self, needed_list_id: int):
        for list_name in self.get_all_symbols_list_name():
            if self.symbols_list.get(list_name).get_id() == needed_list_id:
                return self.symbols_list.get(list_name).get_symbols()

    def __ticker_search(self, ticker: str):
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
    # TODO move this in tickers subclass
    def add_tickers(self, tickers: list):
        """
        Add given tickers list to account.
        tickers - list tickers with format exchange:symbol
        exp: add_tickers(["OANDA:XAUUSD", "BITSTAMP:BTCUSD"])
        """

        add_response = requests.post(self.url_adding, headers=self.headers, data=json.dumps(tickers))
        if add_response.status_code == 200:
            print(add_response.text)
        else:
            raise InvalidURL(f'Warning: \nSomething goes wrong! Response status: ' + str(
                add_response.status_code) + '\nPlease use -h for help and try again.')
    # TODO move this in tickers subclass
    def get_current_tickers(self):
        """
        Return current tickers from account.
        """

        req = requests.get(self.url_curr_tickers, headers=self.headers, cookies=self.cookies_for_search)
        if req.status_code == 200:
            my_tickers = req.json()
            return json.dumps(my_tickers['symbols'], indent=2, sort_keys=True)
        else:
            raise InvalidURL("Cant get all my current tickers. Response status code: " + str(req.status_code))
    # TODO move this in tickers subclass
    def delete_tickers(self, tickers: list):
        """
        Delete given tickers list from account.
        """

        del_response = requests.post(self.url_deleting, headers=self.headers, data=json.dumps(tickers))
        if del_response.status_code == 200:
            print(del_response.text)
        else:
            raise InvalidURL(f'Warning: \nSomething goes wrong! Response status: ' + str(
                del_response.status_code) + '\nPlease use -h for help and try again.')
    # TODO move this in tickers subclass
    def free_all_tickers(self):
        """
        Delete all tickers from account.
        """

        ansver: str = input(
            b_colors.WARNING + "Are you sure, you want delete all you current tickers? Do you make backup? Y/n: " + b_colors.ENDC)
        if ansver == 'Y':
            print(b_colors.OKGREEN + "Deleting shares..." + b_colors.ENDC)
            self.delete_tickers(json.loads(self.get_current_tickers()))
            print(b_colors.OKGREEN + "All pass good! You dashboard cleaned." + b_colors.ENDC)
        if ansver == 'n':
            print(b_colors.FAIL + "Deleting interrupted!" + b_colors.ENDC)

    def repair_ticker_format(self, invalid_ticker: str):
        """
        Get invalid ticker.
        Return suggested valid ticker format.
        """

        if tconfig.exist(invalid_ticker):
            print(b_colors.OKGREEN + 'Ticker ' + invalid_ticker + ' found in config' + b_colors.ENDC)
            return tconfig.get_value(invalid_ticker)
        else:
            print(b_colors.OKCYAN + 'Ticker ' + invalid_ticker + ' getting request' + b_colors.ENDC)
            suggested_ticker = self.__ticker_search(invalid_ticker)
            time.sleep(0.5)
            if suggested_ticker:
                tconfig.write(invalid_ticker, suggested_ticker[0])
                return suggested_ticker[0]
            else:
                print("SOMETHING WITH REQUEST REPAIRED TICKERS")
                return ''

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
