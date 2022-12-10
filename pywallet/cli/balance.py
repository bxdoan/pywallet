#! /usr/bin/env python3
import click
from pywallet.config import Config
from pywallet.constants import ETH_NATIVE_ADDRESS
from pywallet.wallet import Wallet
from pywallet.print import printd
from pywallet.token import Token


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-w', '--wallet-address', 'wallet_address', help="Wallet address", default="", show_default=False)
@click.option('-t', '--token-address', 'token_address', help="Token address", default="Native token", show_default=True)
def balance_handler(token_address: str, wallet_address: str) -> None:
    """Get balance\n
    balance -t <token_address> -w <wallet_address>
    """
    config = Config()
    wallet = Wallet(config.get_keypair_path())

    if not wallet.is_wallet_exited():
        printd(msg="Wallet not found, please create wallet first")
        quit()

    if token_address == "Native token":
        token_address = ETH_NATIVE_ADDRESS

    if wallet_address == "":
        wallet_address = wallet.get_address()

    token = Token(config.get_url(), wallet_address, token_address)

    balance = token.get_balance()
    symbol = token.get_symbol()
    printd(msg="Balance: " + balance + " " + symbol)


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-w', '--wallet-address', 'wallet_address', help="Wallet address", default="", show_default=False)
def balance_all(wallet_address: str) -> None:
    """Get balance all token\n
    balance -t <token_address> -w <wallet_address>
    """
    config = Config()
    wallet = Wallet(config.get_keypair_path())

    if not wallet.is_wallet_exited():
        printd(msg="Wallet not found, please create wallet first")
        quit()

    if wallet_address == "":
        wallet_address = wallet.get_address()

    Token(
            url=config.get_url(),
            wallet_address=wallet_address,
    ).get_balances(config.get_contract_path())

