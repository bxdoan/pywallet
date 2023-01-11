from unittest.mock import MagicMock


class MockBinanceResponse():
    status_code = 200
    content = b'{"symbol": "BTCUSDT", "price": "13330.67000000"}'

    @staticmethod
    def json():
        text = {"symbol": "BTCUSDT", "price": "13330.67000000"}
        return text


MockRequestsGet = MagicMock()
MockRequestsGet.return_value = MockBinanceResponse
