#! /usr/bin/env python3
from pywallet import constants
from web3 import Web3
from pywallet.constants import ETH_NATIVE_ADDRESS, ERC20_ABI
from pywallet.helper import to_checksum_address


class Token(object):
    def __init__(self, url, wallet_address, token_address, **kwargs) -> None:
        self.w3 = kwargs.get("w3", None)
        self.wallet_address = wallet_address
        self.checksum_wallet_address = to_checksum_address(wallet_address)
        self.token_address = token_address
        self.checksum_token_address = to_checksum_address(token_address)

        self._build_w3(url)

    def _build_w3(self, url) -> None:
        if self.w3 is None:
            self.w3 = Web3(Web3.HTTPProvider(url))

    def get_balance(self) -> str:
        if self.token_address == ETH_NATIVE_ADDRESS:
            balance = self.w3.eth.get_balance(self.checksum_wallet_address)
            balance = str(float(balance) / 10 ** 18)
        else:
            contract = self.w3.eth.contract(address=self.checksum_token_address, abi=constants.ERC20_ABI)
            balance = contract.functions.balanceOf(self.checksum_wallet_address).call()
            balance = str(balance / 10 ** self.get_decimal())
        return balance

    def get_symbol(self) -> str:
        if self.token_address == ETH_NATIVE_ADDRESS:
            return "ETH"
        else:
            token = self.w3.eth.contract(address=self.checksum_token_address, abi=constants.ERC20_ABI)
            return token.functions.symbol().call()

    def get_decimal(self) -> int:
        if self.token_address == ETH_NATIVE_ADDRESS:
            return 18
        else:
            contract = self.w3.eth.contract(address=self.checksum_token_address, abi=constants.ERC20_ABI)
            return contract.functions.decimals().call()

    def get_contract(self) -> object:
        return self.w3.eth.contract(address=self.checksum_token_address, abi=constants.ERC20_ABI)

    def get_token_info(self) -> dict:
        token_info = {}
        if len(self.token_address) == 0:
            token_info["address"] = ETH_NATIVE_ADDRESS
            token_info["name"] = "Ethereum"
            token_info["symbol"] = "ETH"
            token_info["decimals"] = "18"
            balance = self.w3.eth.get_balance(self.checksum_wallet_address)
            token_info["balance"] = str(float(balance / 10 ** 18))

        else:
            contract = self.w3.eth.contract(address=self.checksum_token_address, abi=ERC20_ABI)
            token_info["address"] = self.token_address
            token_info["name"] = str(contract.functions.name().call())
            token_info["symbol"] = str(contract.functions.symbol().call())
            token_info["decimals"] = str(contract.functions.decimals().call())
            balance = contract.functions.balanceOf(self.checksum_wallet_address).call()
            token_info["balance"] = str(balance / 10 ** int(token_info["decimals"]))
        return token_info
