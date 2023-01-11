import requests

from pywallet import constants
from pywallet.print import printd
from pywallet.constants import PrintType


class Price(object):

    def __init__(self, **kwargs):
        self.symbol = kwargs.get("symbol", None)

    def get_price(self):
        if isinstance(self.symbol, str):
            # get price from binance
            for sc in constants.StableCoin.all():
                # build url
                url = f"{constants.BNB_API_PRICE}?symbol={self.symbol.upper()}{sc.upper()}"
                # get response
                response = requests.get(url)

                try:
                    # get price
                    resp_json = response.json()
                    price = round(float(resp_json["price"]), 2)
                except KeyError:
                    price = 0

                printd(f"Price of {self.symbol.upper()} is {price} USDT", type_p=PrintType.INFO)
                return price

        return None