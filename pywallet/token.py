#! /usr/bin/env python3
import json
import os
from web3 import Web3

from pywallet.constants import ETH_NATIVE_ADDRESS, ERC20_ABI, HOME_DIR, PrintType, ETH_NATIVE_DECIMAL, \
    ETH_NATIVE_SYMBOL, MATIC_NATIVE_ADDRESS
from pywallet.print import pd
from pywallet import helper


class Token(object):
    def __init__(self, url, wallet_address, token_address=None, **kwargs) -> None:
        self.w3 = kwargs.get("w3", None)
        self.wallet_address = wallet_address
        self.token_address = token_address
        self.checksum_wallet_address = helper.to_checksum_address(wallet_address) if wallet_address else None
        self.checksum_token_address = helper.to_checksum_address(token_address) if token_address else None
        self.list_token = kwargs.get("list_token", None)
        self._build_w3(url)

    def _build_w3(self, url) -> None:
        if self.w3 is None:
            self.w3 = Web3(Web3.HTTPProvider(url))

    def get_balance(self) -> str:
        if self.token_address == ETH_NATIVE_ADDRESS:
            balance = self.w3.eth.get_balance(self.checksum_wallet_address)
            balance = str(float(balance) / 10 ** 18)
        else:
            contract = self.w3.eth.contract(address=self.checksum_token_address, abi=ERC20_ABI)
            balance = contract.functions.balanceOf(self.checksum_wallet_address).call()
            balance = str(balance / 10 ** self.get_decimal())
        return balance

    def get_balances(self, coin_addresses : list = None, network : str = None) -> list:
        default_token = self._get_default_token(network)
        if not coin_addresses:
            coin_addresses = [default_token["address"]]
        else:
            coin_addresses = [default_token["address"]] + coin_addresses
        list_balance = []
        for token_address in coin_addresses:
            if token_address == ETH_NATIVE_ADDRESS:
                balance = self.w3.eth.get_balance(self.checksum_wallet_address)
                balance = str(float(balance) / 10 ** 18)
                default_token.update({
                    "balance": balance
                })
                list_balance.append(default_token)
            else:
                try:
                    contract = self.w3.eth.contract(address=helper.to_checksum_address(token_address), abi=ERC20_ABI)
                    balance = contract.functions.balanceOf(self.checksum_wallet_address).call()
                    if not balance:
                        continue
                    symbol = contract.functions.symbol().call()
                    decimal = contract.functions.decimals().call()
                    balance = str(balance / 10 ** decimal)
                    list_balance.append({
                        "symbol": symbol,
                        "balance": balance,
                        'decimal': decimal,
                        'address': token_address
                    })
                except Exception as e:
                    pd(e, type_p=PrintType.ERROR)
                    pass
        return list_balance

    def _get_default_token(self, network : str = None) -> dict:
        if network == "matic":
            return {
                "address": MATIC_NATIVE_ADDRESS,
                "symbol": "MATIC",
                "decimal": ETH_NATIVE_DECIMAL,
            }
        else:
            return {
                "address": ETH_NATIVE_ADDRESS,
                "symbol": ETH_NATIVE_SYMBOL,
                "decimal": ETH_NATIVE_DECIMAL,
            }

    def get_symbol(self) -> str:
        if self.token_address == ETH_NATIVE_ADDRESS:
            return "ETH"
        else:
            contract = self.w3.eth.contract(address=self.checksum_token_address, abi=ERC20_ABI)
            return contract.functions.symbol().call()

    def get_decimal(self) -> int:
        if self.token_address == ETH_NATIVE_ADDRESS:
            return 18
        else:
            contract = self.w3.eth.contract(address=self.checksum_token_address, abi=ERC20_ABI)
            return contract.functions.decimals().call()

    def get_contract(self) -> object:
        return self.w3.eth.contract(address=self.checksum_token_address, abi=ERC20_ABI)

    def get_token_info(self) -> dict:
        token_info = {}
        if self.token_address == ETH_NATIVE_ADDRESS:
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


class TokenSearch(object):
    def __init__(self, search_key : str = '', network=None) -> None:
        self.search_key = search_key
        self.network = network or 'eth'

    def _load_json_file(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def _load_all_json_file(self, path):
        list_token = []
        for file in os.listdir(path):
            if file.endswith(".json"):
                json_data = self._load_json_file(os.path.join(path, file))
                list_token.append(json_data)
        return list_token

    def _network_is_valid(self):
        list_network = helper.get_list_of_name_dir_in_folder(f"{HOME_DIR}/tokens")
        if self.network.lower() not in list_network:
            return False
        return True

    def search(self, list_token=None) -> list:
        if not self._network_is_valid():
            pd(msg=f"Network {self.network} is not valid", type_p=PrintType.ERROR)
            exit()

        token_dir = f"{HOME_DIR}/tokens/{self.network.lower()}"
        list_token = self._load_all_json_file(token_dir) if list_token is None else list_token
        list_result = []
        for token in list_token:
            if self.search_key.lower() in token["symbol"].lower() or self.search_key.lower() in token["name"].lower():
                list_result.append(token)
        return list_result

    def search_by_address(self, list_token_address=None) -> list:
        if not self._network_is_valid():
            pd(msg=f"Network {self.network} is not valid", type_p=PrintType.ERROR)
            exit()

        token_dir = f"{HOME_DIR}/tokens/{self.network.lower()}"
        list_result = []
        for token_address in list_token_address:
            path_file = os.path.join(token_dir, f"{token_address}.json")
            if os.path.isfile(path_file):
                json_data = self._load_json_file(path_file)
                list_result.append(json_data)
        return list_result
