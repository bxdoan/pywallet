from unittest import mock

from pywallet.prices import Price
from tests.fixtures.mocks import MockRequestsGet


class TestPrice:

    # mock request.get
    @mock.patch("pywallet.prices.requests.get", MockRequestsGet)
    def test_price(self):
        price = Price(symbol="btc").get_price()
        assert price == 13330.67
