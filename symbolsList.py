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
        self.color: str = self.__get_list_info('color')
        self.active: bool = self.__get_list_info('active')
        self.symbols: list = self.__get_list_info('symbols')
        self.type: ListType = self.__get_list_info('type')
        self.name: str = self.__get_list_info('name')
        self.URL = self.__create_URL()

    def __create_URL(self):
        if self.type == 'colored':
            return self.SITE_URL + 'colored/' + self.color
        else:
            return self.SITE_URL + 'custom/' + str(self.id)


    def __get_list_info(self, info: str):
        responce_lists_info = requests.get(self.ALL_LISTS_URL, headers=self.headers)
        if responce_lists_info.status_code == 200:
            for list_info in responce_lists_info.json():
                if self.id == list_info['id']:
                    return list_info[info]
        else:
            raise InvalidURL('Some problem with getting ' + info + ' for tickers list: ' + self.name)
