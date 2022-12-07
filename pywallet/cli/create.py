#! /usr/bin/env python3
import click
from getpass import getpass
from pywallet.wallet import Wallet
from pywallet.config import Config
from pywallet.print import Print


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
def create_wallet():
    """
    Create new keypair\n
    Usage: create
    """
    config = Config()
    wallet = Wallet(config.get_keypair_path())

    if wallet.is_wallet_exited():
        print("Wallet existed, do you want to override (y/n): ")
        is_override = input()

        if is_override != 'y':
            quit()

    Print.print_info("Private key (default for new wallet): ")
    private_key = getpass("")
    
    Print.print_info("Password (len >= 6): ")
    password = getpass("")

    while len(password) < 6:
        Print.print_info("Password (len >= 6): ")
        password = getpass("")

    Print.print_info("Confirm password: ")
    confirm_password = getpass("")

    if confirm_password != password:
        Print.print_error("Password mismatch")
    else:
        new_address = wallet.create_wallet(private_key, password, True)

        Print.print_success("Create new wallet with address " + new_address)
        print("")

