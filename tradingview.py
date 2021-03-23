#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from validator import TickersValidator
from tconfig import TconfigVrapper
from colors import b_colors
import time

config = TconfigVrapper()
validator = TickersValidator()


class TradingView:
    """
    class for represents a client TV
    get/set/update/delete tickers across HTTP  backend server requests
    """

    def __init__(self):
        self.url_curr_tickers: str = 'https://ru.tradingview.com/api/v1/symbols_list/active/'
        self.url_adding: str = 'https://ru.tradingview.com/api/v1/symbols_list/custom/19681992/append/'
        self.url_deleting: str = 'https://ru.tradingview.com/api/v1/symbols_list/custom/19681992/remove/'
        self.cookies_for_search: dict = {
            'cookie': '_sp_id.cf1a=2b7f734a-07bf-4ee5-8a23-76e7da695f98.1613237271.142.1615548626.1615545423.6bf1ab93-5564-4f63-ada8-c04853135f59; sessionid=djidz6wslxnw510erzs6abto6o3bvk4u; tv_ecuid=eaf43895-763b-41ff-ba93-a5686abe49d4; png=eaf43895-763b-41ff-ba93-a5686abe49d4; etg=eaf43895-763b-41ff-ba93-a5686abe49d4; cachec=eaf43895-763b-41ff-ba93-a5686abe49d4; backend=test_backend; _sp_ses.cf1a=*'}
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
            "Cookie": "_sp_id.cf1a=2b7f734a-07bf-4ee5-8a23-76e7da695f98.1613237271.146.1615576298.1615574319.6263c3c3-9a1e-43e4-9607-11ef3dee49e6; sessionid=djidz6wslxnw510erzs6abto6o3bvk4u; tv_ecuid=eaf43895-763b-41ff-ba93-a5686abe49d4; png=eaf43895-763b-41ff-ba93-a5686abe49d4; etg=eaf43895-763b-41ff-ba93-a5686abe49d4; cachec=eaf43895-763b-41ff-ba93-a5686abe49d4; backend=test_backend; _sp_ses.cf1a=*",
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

    """
    ticker - ticker in string format for search
    return - list suggestion  in format - exchange:symbol
    """

    def ticker_search(self, ticker: str):
        url_search = f'https://symbol-search.tradingview.com/symbol_search/?text={ticker}&hl=1&exchange=&lang=ru&type=&domain=production'
        suggestion_tickers = requests.get(url_search, headers=self.headers_for_search, cookies=self.cookies_for_search)
        if suggestion_tickers.status_code == 200:
            tickers_dict: dict = json.loads(suggestion_tickers.text)
            tickers_resp = []
            for ticker_dict in tickers_dict:
                symbol = ticker_dict['symbol'].replace(u'<em>', u'').replace(u'</em>', u'')
                tickers_resp.append(ticker_dict['exchange'] + ":" + symbol)
            return tickers_resp
        else:
            return []

    """
    Add given tickers list to account.
    tickers - list tickers with format exchange:symbol
    exp: add_tickers(["OANDA:XAUUSD", "BITSTAMP:BTCUSD"])    
    """

    def add_tickers(self, tickers: list):
        add_response = requests.post(self.url_adding, headers=self.headers, data=json.dumps(tickers))
        if add_response.status_code == 200:
            print(add_response.text)
        else:
            print(f'Warning: \nSomething goes wrong! Response status: ' + str(
                add_response.status_code) + '\nPlease use -h for help and try again.')

    """
    Return current tickers from account.
    """

    def get_current_tickers(self):
        req = requests.get(self.url_curr_tickers, headers=self.headers, cookies=self.cookies_for_search)
        my_tickers = req.json()
        return json.dumps(my_tickers['symbols'])

    """
    Delete given tickers list from account.
    """

    def delete_tickers(self, tickers: list):
        del_response = requests.post(self.url_deleting, headers=self.headers, data=json.dumps(tickers))
        if del_response.status_code == 200:
            print(del_response.text)
        else:
            print(f'Warning: \nSomething goes wrong! Response status: ' + str(
                del_response.status_code) + '\nPlease use -h for help and try again.')

    """
    Delete all tickers from account.
    """

    def free_all_tickers(self):
        ansver = input(
            b_colors.WARNING + "Are you sure, you want delete all you current tickers? Do you make backup? Y/n: " + b_colors.ENDC)
        if ansver == 'Y':
            print(b_colors.OKGREEN + "Deleting shares..." + b_colors.ENDC)
            self.delete_tickers(json.loads(self.get_current_tickers()))
            print(b_colors.OKGREEN + "All pass good! You dashboard cleaned." + b_colors.ENDC)
        if ansver == 'n':
            print(b_colors.FAIL + "Deleting interrupted!" + b_colors.ENDC)

    """
    Get invalid ticker.
    Return suggested valid ticker format.
    """

    def repair_ticker_format(self, invalid_ticker: str):
        print(invalid_ticker)
        if config.check_ticker_in_tconfig(invalid_ticker):
            print('дебаг нашли тикер в конфиге')
            return config.get_tickers_list_config().get(invalid_ticker)
        else:
            print('дебаг делаем запрос')
            suggested_ticker = self.ticker_search(invalid_ticker)
            time.sleep(0.3)
            print('дебаг тикер из запроса')
            print(suggested_ticker)
            if suggested_ticker:
                # добавляем тикер в конфиг
                config.write_in_config(invalid_ticker, suggested_ticker[0])
                return suggested_ticker[0]
            else:
                print("SOMETHING WITH REQUEST REPAIRED TICKERS")
                return ''

    """
    Restoring tickers list after validate.
    """

    def restore_tickers_list(self, tickers: list, invalid_tickers: list):
        if invalid_tickers:
            for invalid_ticker in invalid_tickers:
                tickers.remove(invalid_ticker)
                tickers.append(self.repair_ticker_format(invalid_ticker))
            return tickers
        else:
            print('No one invalid tickers found')
            return tickers
