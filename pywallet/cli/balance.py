#! /usr/bin/env python3
from getpass import getpass

import click
from pywallet.config import Config
from pywallet.constants import ETH_NATIVE_ADDRESS, PrintType, NEAR_SYMBOL
from pywallet.wallet import Wallet, NearWallet
from pywallet.print import printd
from pywallet.token import Token


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-w', '--wallet-address', 'wallet_address', help="Wallet address", default="", show_default=False)
@click.option('-t', '--token-address', 'token_address', help="Token address", default="Native token", show_default=True)
@click.option('-n', '--network', 'network', help="Network (default for eth)", default='', show_default=True)
def balance_handler(token_address : str, wallet_address : str, network : str) -> None:
    """Get balance\n
    balance -t <token_address> -w <wallet_address>
    """
    config = Config()

    if network == NEAR_SYMBOL.lower() or config.get_network() == NEAR_SYMBOL.lower():
        printd("Type your password: ")
        password = getpass("")
        near_wallet = NearWallet(
            keypair_path = config.get_keypair_near_path(),
            password=password
        )
        balance = near_wallet.get_balance(address=wallet_address, token_address=token_address)
        symbol = NEAR_SYMBOL if not token_address else near_wallet.get_symbols(token_address=token_address)
    else:
        wallet = Wallet(config.get_keypair_path())

        if not wallet.is_wallet_exited():
            printd(msg="Wallet not found, please create wallet first\n use command: create", type_p=PrintType.ERROR)
            quit()

        if token_address == "Native token":
            token_address = ETH_NATIVE_ADDRESS

        if wallet_address == "":
            wallet_address = wallet.get_address()

        token = Token(config.get_url(network), wallet_address, token_address)
        balance = token.get_balance()
        symbol = token.get_symbol()

    if balance is None:
        printd(msg="Balance not found", type_p=PrintType.ERROR)
        quit()
    printd(msg="Balance: " + balance + " " + symbol)


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-w', '--wallet-address', 'wallet_address', help="Wallet address", default="", show_default=False)
def balance_all(wallet_address: str) -> None:
    """Get balance all token\n
    balance-all -w <wallet_address>
    """
    config = Config()
    wallet = Wallet(config.get_keypair_path())

    if not wallet.is_wallet_exited():
        printd(msg="Wallet not found, please create wallet first\n use command: create", type_p=PrintType.ERROR)
        quit()

    if wallet_address == "":
        wallet_address = wallet.get_address()

    network = config.get_config()["network"]
    list_balance = Token(
        url=config.get_url(),
        wallet_address=wallet_address,
    ).get_balances(coin_addresses=config.get_coin_list(), network=network)
    for balance in list_balance:
        printd(msg="Balance: " + balance['balance'] + " " + balance['symbol'])
