import requests
import argparse
import json
import sys
from validator import validate_format
from tradingview import TradingView
import tconfig
from colors import b_colors

trading_view = TradingView()

parser = argparse.ArgumentParser(description='This is CLI client for tradingview.com',
                                 epilog='Enjoy!')


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


def working_with_args():
    if cli_args().backup:
        print(trading_view.get_current_tickers())

    if cli_args().load:
        if not sys.stdin.isatty():
            valid_list = []
            for ticker in json.load(sys.stdin):
                if validate_format(ticker):
                    valid_list.append(ticker)
                else:
                    valid_list.append(trading_view.repair_ticker_format(ticker))
            for ticker in valid_list:
                print("передаю этот тикер " + ticker)
            trading_view.add_tickers(valid_list)
        else:
            print(
                f"{b_colors.FAIL}Warning: \nNo any tickers have not found ! Please use -h for help and try again.{b_colors.ENDC} "
            )
    if cli_args().free:
        trading_view.free_all_tickers()


def main():
    add_cli_args()
    tconfig.load_from_file()
    working_with_args()
    tconfig.save()


if __name__ == '__main__':
    main()
