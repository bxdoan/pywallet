import requests

from pywallet import constants


class Price(object):

    def __init__(self, **kwargs):
        self.symbol = kwargs.get("symbol", None)

    def get_price(self):
        if isinstance(self.symbol, str):
            # get price from binance
            for sc in constants.StableCoin.all():
                # build url
                url = f"{constants.BNB_API_PRICE}?symbol={self.symbol.upper()}{sc.upper()}"

                try:
                    # get response
                    response = requests.get(url)

                    # get price
                    resp_json = response.json()
                    price = round(float(resp_json["price"]), 2)
                except KeyError:
                    price = 0

                if price > 0:
                    # if price is found, return it, otherwise continue
                    return price

        return None
