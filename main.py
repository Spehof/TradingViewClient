import requests
import argparse
import json
import sys
import re
import time
from validator import  TickersValidator
from tradingview import TradingView
from tconfig import TconfigVrapper

config = TconfigVrapper()
trading_view = TradingView()
ticker_validator = TickersValidator()


URL = 'https://ru.tradingview.com/api/v1/symbols_list/active/'
HEADERS = {
    'accept': '*/*',
    'x-language': 'en',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}
COOKIES = {
    'cookie': '_sp_id.cf1a=2b7f734a-07bf-4ee5-8a23-76e7da695f98.1613237271.142.1615548626.1615545423.6bf1ab93-5564-4f63-ada8-c04853135f59; sessionid=djidz6wslxnw510erzs6abto6o3bvk4u; tv_ecuid=eaf43895-763b-41ff-ba93-a5686abe49d4; png=eaf43895-763b-41ff-ba93-a5686abe49d4; etg=eaf43895-763b-41ff-ba93-a5686abe49d4; cachec=eaf43895-763b-41ff-ba93-a5686abe49d4; backend=test_backend; _sp_ses.cf1a=*'}

parser = argparse.ArgumentParser(description='This is CLI client for tradingview.com',
                                 epilog='Enjoy!')
tconfig = {}


class b_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def add_cli_args():
    global parser
    parser.add_argument('-b', '--backup',
                        help='Get all current tickers to stdout',
                        action='store_true')
    parser.add_argument('-p', '--ping',
                        help='Check connection to site with current cookie',
                        action='store_true')
    parser.add_argument('-f', '--free',
                        help='Remove all tickers from symbols list',
                        action='store_true')
    parser.add_argument('-c', '--cookie',
                        help='Get own cookie',
                        action='store_true')
    parser.add_argument('-l', '--load',
                        type=str,
                        nargs='?',
                        help='Load all tickers to TradingView symbols list from stdin',
                        const=sys.stdin,
                        )

    def validate_format(tickers: list):
        formatted_list = []
        valid_tickers_pattern = re.compile("[A-Z]+:[A-Z]+")
        for ticker in tickers:
            if not valid_tickers_pattern.findall(ticker):
                print('INVALID TICKER => ' + ticker)
                formatted_list.append(trading_view.repair_ticker_format(ticker))
            else:
                formatted_list.append(ticker)
        return formatted_list

def cli_args():
    args = parser.parse_args()
    return args


def ticker_search(ticker: str):
    """
    ticker - ticker in string format for search
    return - list suggestion  in format - exchange:symbol
    """
    url_search = f'https://symbol-search.tradingview.com/symbol_search/?text={ticker}&hl=1&exchange=&lang=ru&type=&domain=production'
    suggestion_tickers = requests.get(url_search, headers=HEADERS, cookies=COOKIES)
    if suggestion_tickers.status_code == 200:
        tickers_dict: dict = json.loads(suggestion_tickers.text)
        tickers_resp = []
        for ticker_dict in tickers_dict:
            symbol = ticker_dict['symbol'].replace(u'<em>', u'').replace(u'</em>', u'')
            tickers_resp.append(ticker_dict['exchange'] + ":" + symbol)
        return tickers_resp
    else:
        return []

def load_config():
    global tconfig
    try:
        with open('tconfig.json') as f:
            tconfig = json.load(f)
    except IOError:
        print(b_colors.FAIL + "File tconfig not accessible! Please check file: tconfig.json" + b_colors.ENDC)
    finally:
        f.close()



def check_ticker_in_tconfig(ticker: str):
    if ticker in tconfig.keys():
        return True
    else:
        return False



def repair_format(invalid_ticker: str):
    if check_ticker_in_tconfig(invalid_ticker):
        return tconfig.get(invalid_ticker)
    else:
        suggested_ticker = ticker_search(invalid_ticker)
        time.sleep(0.3)
        if suggested_ticker:
            # добавляем тикер в конфиг
            tconfig[invalid_ticker] = suggested_ticker[0]
            return suggested_ticker[0]
        else:
            print("SOMETHING WITH REQUEST REPAIRED TICKERS")
            return ''


def validate_format(tickers: list):
    formatted_list = []
    valid_tickers_pattern = re.compile("[A-Z]+:[A-Z]+")
    for ticker in tickers:
        if not valid_tickers_pattern.findall(ticker):
            print('INVALID TICKER => ' + ticker)
            formatted_list.append(trading_view.repair_ticker_format(ticker))
        else:
            formatted_list.append(ticker)
    return formatted_list


def ping():
    # TODO: write getting account name
    pass


def add_tickers(tickers: list):
    """
    tickers - list tickers with format exchange:symbol
    exp: add_tickers(["OANDA:XAUUSD", "BITSTAMP:BTCUSD"])
    """
    url_adding = 'https://ru.tradingview.com/api/v1/symbols_list/custom/19681992/append/'
    adding_headers: dict = {
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
    add_response = requests.post(url_adding, headers=adding_headers, data=json.dumps(tickers))
    print(add_response.text)
    if add_response.status_code == 200:
        print(add_response.text)
    else:
        print(f'Warning: \nSomething goes wrong! Response status: ' + str(
            add_response.status_code) + '\nPlease use -h for help and try again.')


def get_current_tickers():
    req = requests.get(URL, headers=HEADERS, cookies=COOKIES)
    my_tickers = req.json()
    return json.dumps(my_tickers['symbols'])


def delete_tickers(tickers: list):
    url_adding = 'https://ru.tradingview.com/api/v1/symbols_list/custom/19681992/remove/'
    adding_headers: dict = {
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
    del_response = requests.post(url_adding, headers=adding_headers, data=json.dumps(tickers))
    if del_response.status_code == 200:
        print(del_response.text)
    else:
        print(f'Warning: \nSomething goes wrong! Response status: ' + str(
            del_response.status_code) + '\nPlease use -h for help and try again.')

def write_all_new_tickers_in_tconfig():
    with open('tconfig.json', 'w') as f:
        json.dump(tconfig, f, indent=2, sort_keys=True)


def main():
    if cli_args().backup:
        print(trading_view.get_current_tickers())

    if cli_args().load:
        if not sys.stdin.isatty():
            # trading_view.add_tickers(["BITSTAMP:BTCUSD"])
            # TODO add validation and restore format with JSON file
            trading_view.add_tickers(json.load(sys.stdin))
        else:
            print(
                f"{b_colors.FAIL}Warning: \nNo any tickers have not found ! Please use -h for help and try again.{b_colors.ENDC} "
            )
    if cli_args().free:
        trading_view.free_all_tickers()


if __name__ == '__main__':
    add_cli_args()
    config.load_from_file()
    main()
    config.refresh()
# TODO: writing in file
# TODO: refactor all this shit to classes
