import requests
import argparse
import json
import sys

URL = 'https://ru.tradingview.com/api/v1/symbols_list/active/'
HEADERS = {
    'accept': '*/*',
    'x-language': 'en',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}
COOKIES = {
    'cookie': '_sp_id.cf1a=2b7f734a-07bf-4ee5-8a23-76e7da695f98.1613237271.142.1615548626.1615545423.6bf1ab93-5564-4f63-ada8-c04853135f59; sessionid=djidz6wslxnw510erzs6abto6o3bvk4u; tv_ecuid=eaf43895-763b-41ff-ba93-a5686abe49d4; png=eaf43895-763b-41ff-ba93-a5686abe49d4; etg=eaf43895-763b-41ff-ba93-a5686abe49d4; cachec=eaf43895-763b-41ff-ba93-a5686abe49d4; backend=test_backend; _sp_ses.cf1a=*'}

parser = argparse.ArgumentParser(description='This is CLI client for tradingview.com',
                                 epilog='Enjoy!'
                                 )


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


def cli_args():
    args = parser.parse_args()
    return args


def validate_format(tickers):
    # TODO: write checking format tickers
    return tickers


def ping():
    # TODO: write getting account name
    pass


def ticker_search(ticker: str):
    """
    ticker - ticker in string format for search
    return - list suggestion  in format - exchange:symbol
    """
    url_search = f'https://symbol-search.tradingview.com/symbol_search/?text={ticker}&hl=1&exchange=&lang=ru&type=&domain=production'
    suggestion_tickers = requests.get(url_search, headers=HEADERS, cookies=COOKIES)
    tickers_dict: dict = json.loads(suggestion_tickers.text)
    tickers_resp = []
    for ticker_dict in tickers_dict:
        symbol = ticker_dict['symbol'].replace(u'<em>', u'').replace(u'</em>', u'')
        tickers_resp.append(ticker_dict['exchange'] + ':' + symbol)
    return tickers_resp


def add_tickers(tickers):
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
    if add_response.status_code == 200:
        print(add_response.text)
    else:
        print(
            f"{b_colors.FAIL}Warning: \nSomething goes wrong! Response status: " + add_response.status_code + "\nPlease use -h for help and try again.{b_colors.ENDC}")


def get_current_tickers():
    req = requests.get(URL, headers=HEADERS, cookies=COOKIES)
    my_tickers: dict = json.loads(req.text)
    print(my_tickers['symbols'])


def delete_tickers():
    # TODO: write delete tickers
    pass


def main():
    if cli_args().backup:
        get_current_tickers()

    if cli_args().load:
        if not sys.stdin.isatty():
            add_tickers(validate_format(json.load(sys.stdin)))
        else:
            print(
                f"{b_colors.FAIL}Warning: \nNo any tickers have not found ! Please use -h for help and try again.{b_colors.ENDC} "
            )

    if cli_args().free:
        delete_tickers(get_current_tickers())

        # print(ticker_search('GOOG'))
        # add_tickers(["OANDA:XAUUSD", "BITSTAMP:BTCUSD"])


if __name__ == '__main__':
    add_cli_args()
    main()
