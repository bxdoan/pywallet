from unittest import TestCase
from unittest.mock import patch, MagicMock

import pytest

from pywallet import Config
from pywallet.constants import ETH_NATIVE_ADDRESS
from pywallet.token import Token
from pywallet.wallet import Wallet

TOKEN_NAME = "BuiCoin"
TOKEN_SYMBOL = "BUI"
TOKEN_DECIMALS = 18
TOKEN_INITIAL_SUPPLY = 0


@pytest.fixture
def wallet_contract(w3, get_contract):
    code = """
@external
@view
def get_balance() -> uint256:
    a: uint256 = self.balance
    return a

@external
@payable
def __default__():
    pass
    """
    contract = get_contract(code, *[w3.eth.accounts[0]])
    return contract


@pytest.fixture
def token_cont(w3, get_contract):
    code = """
name: public(String[32])
symbol: public(String[32])
decimals: public(uint8)

@external
def __init__(_name: String[32], _symbol: String[32], _decimals: uint8):
    self.name = _name
    self.symbol = _symbol
    self.decimals = _decimals

@external
def get_balance() -> uint256:
    a: uint256 = self.balance
    return a

    """
    c = get_contract(code, *[TOKEN_NAME, TOKEN_SYMBOL, TOKEN_DECIMALS])
    return c


# @patch('pywallet.wallet.Wallet.get_address', MagicMock(return_value=wallet_contract.address))
def test_transfer(w3, wallet_contract):
    receiver_address = '0x4e65175f05b4140a0747c29cce997cd4bb7190d4'  # my wallet
    url = 'https://some_url.com'  # mainnet

    config = {
        'url': {
            "eth": url
        },
        'keypair_path': "/tmp/keypair.json",
    }
    wallet = Wallet(
        keypair_path=config['keypair_path'],
        url=url,
        w3=w3,
    )
    wallet.create_wallet(private_key='', password='123456')
    private_key = wallet.get_private_key('123456')

    value = 14000000000000000000 * 10 ^ 18
    w3.eth.send_transaction({"to": wallet_contract.address, "value": value})

    # check symbol
    t = Token(
        w3=w3,
        url=url,
        wallet_address=wallet_contract.address,
        token_address=ETH_NATIVE_ADDRESS,
    )
    assert t.get_symbol() == "ETH"
    balance = t.get_balance()
    assert balance == f'{value / 10 ** 18}'

    token_info = t.get_token_info()
    transfer_params = {
        'token_info': token_info,
        'amount': 1 * 10 ^ 18,
        'private_key': private_key,
        'sender': wallet_contract.address,
        'receiver': receiver_address,
    }
    trans_hash = wallet.transfer_token(**transfer_params)
    assert trans_hash
