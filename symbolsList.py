import json
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
        self.__id: int = list_id
        # __tickers_list_data = json object with data about list_tickers (for caching data)
        self.__tickers_list_data = self.__get_list_info()

        self.__color: str = self.__tickers_list_data['color']
        self.__active: bool = self.__tickers_list_data['active']
        self.__symbols: list = self.__tickers_list_data['symbols']
        self.__type: ListType = self.__tickers_list_data['type']
        self.__name: str = self.__tickers_list_data['name']
        self.__URL: str = self.__create_URL()
        self.__URL_remove: str = self.__create_URL_remove()

    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_type(self) -> ListType:
        return self.__type

    def get_URL(self) -> str:
        return self.__URL

    def get_tickers(self) -> list:
        return self.__symbols

    def get_active(self) -> bool:
        return self.__active

    def delete_tickers(self, tickers_list: list):
        del_response = requests.post(self.__URL_remove, headers=self.headers, data=json.dumps(tickers_list))
        if del_response.status_code == 200:
            print(del_response.text)
        else:
            raise InvalidURL(f'Warning: \nSomething with deleting tickers goes wrong! Response status: ' + str(
                del_response.status_code) + '\nPlease use -h for help and try again.')

    def __get_list_info(self):
        responce_lists_info = requests.get(self.ALL_LISTS_URL, headers=self.headers)
        if responce_lists_info.status_code == 200:
            for list_info in responce_lists_info.json():
                if self.__id == list_info['id']:
                    return list_info
        else:
            raise InvalidURL('Some problem with getting tickers_list_data for tickers list: ' + self.__name)

    def __create_URL(self) -> str:
        if self.__type == 'colored':
            return self.SITE_URL + 'colored/' + self.__color + '/'
        else:
            return self.SITE_URL + 'custom/' + str(self.__id) + '/'

    def __create_URL_remove(self) -> str:
        return self.__URL + 'remove'  + '/'

