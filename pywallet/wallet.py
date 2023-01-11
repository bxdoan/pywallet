#! /usr/bin/env python3
import asyncio
import os
import secrets
import json
from eth_account import Account as AccountEth
from pynear.account import Account as AccountNear
from web3 import Web3

from pywallet import constants, auth
from pywallet import helper
from pywallet.print import pd


class Wallet(object):
    def __init__(self, keypair_path: str, url : str = None, **kwargs) -> None:
        self.keypair_path = keypair_path
        self.url = url

        self.w3 = kwargs.get("w3", None)
        self._build_w3(url)

    def _build_w3(self, url) -> None:
        if self.w3 is None and url is not None:
            self.w3 = Web3(Web3.HTTPProvider(url))

    def load_keypair_encrypted(self):
        with open(self.keypair_path, "r") as f:
            keypair_encrypted = json.load(f)
        return keypair_encrypted

    def is_wallet_exited(self) -> bool:
        if not os.path.isfile(self.keypair_path):
            return False
        else:
            return True

    def get_address(self):
        keypair_encrypted = self.load_keypair_encrypted()
        return "0x" + keypair_encrypted["address"]

    def get_private_key(self, password: str) -> str:
        keypair_encrypted = self.load_keypair_encrypted()
        try:
            private_key = AccountEth.decrypt(keypair_encrypted, password)
            return private_key
        except ValueError:
            pd(msg="Wrong password", type_p=constants.PrintType.ERROR)
            exit()

    def create_wallet(self, private_key: str, password: str) -> str:
        if len(private_key) < 32:
            private_key = "0x" + secrets.token_hex(32)

        account = AccountEth.from_key(private_key)
        encrypted_key = AccountEth.encrypt(private_key, password = password)
        json_object = json.dumps(encrypted_key, indent = 4)
        with open(self.keypair_path, "w+") as outfile:
            outfile.write(json_object)
        
        return account.address

    def transfer_token(self, token_info : dict, amount : float, private_key : str, receiver : str) -> str:
        try:
            address = self.get_address()
            checksum_token = helper.to_checksum_address(token_info["address"])
            contract = self.w3.eth.contract(address=checksum_token, abi=constants.ERC20_ABI)
            amount = int(amount * (10 ** int(token_info["decimals"])))
            check_address = helper.to_checksum_address(address)
            nonce = self.w3.eth.getTransactionCount(check_address)
            gas_params = {
                'nonce': nonce,
                'gas': 70000,
                'gasPrice': self.w3.toWei('10', 'gwei'),
            }
            checksum_receiver = helper.to_checksum_address(receiver)
            transfer = contract.functions.transfer(checksum_receiver, amount)
            transaction = transfer.buildTransaction(gas_params)
            signed_txn = self.w3.eth.account.signTransaction(transaction, private_key=private_key)
            self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            return signed_txn.hash
        except Exception as e:
            pd(msg=e, type_p=constants.PrintType.ERROR)
            return None


class NearWallet(object):

    def __init__(
            self,
            keypair_path : str = '',
            password : str = '',
            account_id: str = '',
            private_key : str = None,
            **kwargs
    ) -> None:
        self.keypair_path = keypair_path
        self.password = password

        self.account_id = account_id or self.get_account_id_from_keypair_path()
        self.private_key = private_key or self.get_private_key()

        self.acc = kwargs.get("acc", None)
        self._build_acc()

    def _build_acc(self):
        self.acc = AccountNear(self.account_id, private_key=self.private_key)
        asyncio.run(self.acc.startup())

    def get_private_key(self) -> str:
        keypair_encrypted = self.load_keypair_encrypted()
        try:
            private_key = auth.decrypt_(self.password, keypair_encrypted['encrypted_key'])
            return private_key
        except ValueError:
            pd(msg="Wrong password", type_p=constants.PrintType.ERROR)
            exit()

    def get_account_id_from_keypair_path(self) -> str:
        keypair_encrypted = self.load_keypair_encrypted()
        return keypair_encrypted['account_id']

    def load_keypair_encrypted(self):
        with open(self.keypair_path, "r") as f:
            keypair_encrypted = json.load(f)
        return keypair_encrypted

    def dump_keypair_encrypted(self, json_params: dict) -> None:
        with open(self.keypair_path, "w+") as outfile:
            json_object = json.dumps(json_params, indent=4)
            outfile.write(json_object)

    def get_balance(self, address : str = None, token_address : str = None) -> str:
        if not address:
            address = self.account_id

        try:
            if token_address:
                token_info = self.get_token_info(token_address)
                balance = asyncio.run(self.acc.view_function(token_address, 'ft_balance_of',
                                                             {'account_id': address})).result
                balance = float(balance) / (10 ** int(token_info['decimals']))
                return f"{balance}"
            else:
                balance = asyncio.run(self.acc.get_balance(address))
                if balance:
                    # format yoctoNEAR
                    balance = str(balance / constants.NEAR)
                    return balance

            return ''
        except Exception as e:
            pd(msg=e, type_p=constants.PrintType.ERROR)
            return ''

    def get_token_info(self, token_address) -> dict:
        token_info = asyncio.run(self.acc.view_function(token_address, 'ft_metadata', {})).result
        return token_info

    def get_symbols(self, token_address) -> str:
        token_info = self.get_token_info(token_address)
        return token_info['symbol']

    def create_wallet(self, password: str) -> str:
        encrypted_key = auth.encrypt_(password, self.private_key)
        json_params = {
            "account_id": self.account_id,
            "encrypted_key": encrypted_key,
        }
        self.dump_keypair_encrypted(json_params)
        return self.acc.signer.account_id
