import requests
import argparse
import json
import sys

def add_args():
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
                        help='Load all tickers to TradingView symbols list from stdin',
                        action='store_true')


def cli_args():
    args = parser.parse_args()
    return args

def get_current_tickers():
    req = requests.get(URL,headers=HEADERS, cookies=COOKIES)
    jsonq:dict = json.loads(req.text)
    print(jsonq['symbols'])

def main():
    if cli_args().backup:
        get_current_tickers()

if __name__ == '__main__':

    URL = 'https://ru.tradingview.com/api/v1/symbols_list/active/'
    HEADERS = {
        'accept': '*/*',
        'x-language': 'en',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
               }
    COOKIES = {'cookie' : '_sp_id.cf1a=2b7f734a-07bf-4ee5-8a23-76e7da695f98.1613237271.142.1615548626.1615545423.6bf1ab93-5564-4f63-ada8-c04853135f59; sessionid=djidz6wslxnw510erzs6abto6o3bvk4u; tv_ecuid=eaf43895-763b-41ff-ba93-a5686abe49d4; png=eaf43895-763b-41ff-ba93-a5686abe49d4; etg=eaf43895-763b-41ff-ba93-a5686abe49d4; cachec=eaf43895-763b-41ff-ba93-a5686abe49d4; backend=test_backend; _sp_ses.cf1a=*'}
    parser = argparse.ArgumentParser(description='This is CLI client for tradingview.com')
    main()
