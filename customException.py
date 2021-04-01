from requests import RequestException


class TickersListNotExist(Exception):
    pass


class TickerSearchException(RequestException):
    pass


class DeleteTickerException(RequestException):
    pass


class AddTickerException(RequestException):
    pass


class GetListInfoException(RequestException):
    pass
