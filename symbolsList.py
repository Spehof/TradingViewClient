from enum import Enum
import requests
from requests.exceptions import InvalidURL
from cookieLoader import get_cookie

ListType = Enum('custom', 'colored')


class SymbolsList:
    SITE_URL = 'https://www.tradingview.com/api/v1/symbols_list/'
    ALL_LISTS_URL = 'https://www.tradingview.com/api/v1/symbols_list/all/'
    headers: dict = {
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

    def __init__(self,
                 list_id: int):

        self.id: int = list_id
        self.tickers_list_data = self.__get_list_info()
        self.color: str = self.tickers_list_data['color']
        self.active: bool = self.tickers_list_data['active']
        self.symbols: list = self.tickers_list_data['symbols']
        self.type: ListType = self.tickers_list_data['type']
        self.name: str = self.tickers_list_data['name']
        self.URL = self.__create_URL()

    def __create_URL(self):
        if self.type == 'colored':
            return self.SITE_URL + 'colored/' + self.color
        else:
            return self.SITE_URL + 'custom/' + str(self.id)


    def __get_list_info(self):
        responce_lists_info = requests.get(self.ALL_LISTS_URL, headers=self.headers)
        if responce_lists_info.status_code == 200:
            for list_info in responce_lists_info.json():
                if self.id == list_info['id']:
                    return list_info
        else:
            raise InvalidURL('Some problem with getting tickers_list_data for tickers list: ' + self.name)
