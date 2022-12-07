#! /usr/bin/env python3
import click
from getpass import getpass
from pywallet.wallet import Wallet
from pywallet.config import Config
from pywallet.print import printd


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
def create_wallet():
    """
    Create new keypair\n
    Usage: create
    """
    config = Config()
    wallet = Wallet(config.get_keypair_path())

    if wallet.is_wallet_exited():
        printd("Wallet existed, do you want to override (y/n): ")
        is_override = input()

        if is_override != 'y':
            quit()

    printd("Private key (default for new wallet): ")
    private_key = getpass("")
    
    printd("Password (len >= 6): ")
    password = getpass("")

    while len(password) < 6:
        printd("Password (len >= 6): ")
        password = getpass("")

    printd("Confirm password: ")
    confirm_password = getpass("")

    if confirm_password != password:
        printd("Password mismatch")
    else:
        new_address = wallet.create_wallet(private_key, password, True)
        printd("Create new wallet with address " + new_address)

