#! /usr/bin/env python3
from getpass import getpass
import click

from pywallet.config import Config
from pywallet.constants import ETH_NATIVE_ADDRESS, PrintType
from pywallet.print import printd
from pywallet.token import Token
from pywallet.wallet import Wallet


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument("receiver", type=str)
@click.argument("amount", type=float)
@click.option('-t', '--token-address', 'token_address', help="Token Address", default="Native token", show_default=True)
def transfer_handler(receiver: str, amount: float, token_address: str):
    """Transfer for wallet\n
    transfer <receiver> <amount>\n
    transfer <receiver> <amount> -t <token-address>\n
    """
    config = Config().get_config()
    wallet = Wallet(**config)
    if token_address == "Native token":
        token_address = ETH_NATIVE_ADDRESS

    token = Token(url=config['url'], wallet_address=wallet.get_address(), token_address=token_address)

    printd("Password: ")
    password = getpass("")

    balance = token.get_balance()
    symbol = token.get_symbol()
    printd(msg=balance + " " + symbol)
    printd(msg="Transferring...")

    transfer_params = {
        'token_info': token.get_token_info(),
        'amount': amount,
        'private_key': wallet.get_private_key(password),
        'receiver': receiver,
    }
    trans_hash = wallet.transfer_token(**transfer_params)
    if trans_hash:
        printd("Transfer successfully", type_p=PrintType.SUCCESS)
        printd(f"Transaction hash: " + "123")

