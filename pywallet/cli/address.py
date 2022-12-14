#! /usr/bin/env python3
import click
from pywallet.config import Config
from pywallet.constants import PrintType
from pywallet.wallet import Wallet
from pywallet.print import pd


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
def get_address():
    """
    Get your wallet address\n
    Usage: address
    """
    config = Config()
    wallet = Wallet(config.get_keypair_path())

    if not wallet.is_wallet_exited():
        pd(msg="Wallet not found, please create wallet first\n use command: create", type_p=PrintType.ERROR)
        quit()
    address = wallet.get_address()
    pd(msg="Address: " + address, type_p=PrintType.SUCCESS)
