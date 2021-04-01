from requests import RequestException


class TickersListNotExist(Exception):
    pass


class TickerSearchException(RequestException):
    pass
