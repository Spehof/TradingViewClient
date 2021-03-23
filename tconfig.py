import json
from colors import b_colors


class TconfigVrapper:

    def __init__(self):
        self.tickers_list: dict = {}

    def load_from_file(self):
        try:
            with open('tconfig.json') as f:
                self.tickers_list = json.load(f)
        except IOError:
            print(b_colors.FAIL + "File tconfig not accessible! Please check file: tconfig.json" + b_colors.ENDC)
        finally:
            f.close()

    def refresh(self):
        with open('tconfig.json', 'w') as f:
            json.dump(self.tickers_list, f, indent=2, sort_keys=True)

    def check_ticker_in_tconfig(self, ticker: str):
        if ticker in self.tickers_list.keys():
            return True
        else:
            return False

    def get_tickers_list_config(self):
        return self.tickers_list

    def write_in_config(self, invalid_tickers_name: str, suggested_ticker: str):
        self.tickers_list[invalid_tickers_name] = suggested_ticker
