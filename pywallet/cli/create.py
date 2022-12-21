#! /usr/bin/env python3
import click
from getpass import getpass

from pywallet import helper
from pywallet.constants import NEAR_SYMBOL
from pywallet.wallet import Wallet, NearWallet
from pywallet.config import Config
from pywallet.print import printd


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
def create_wallet():
    """
    Create new keypair\n
    Usage: create
    """
    config = Config()
    printd("Create key for network? (evm/near) (default for evm wallet (eth/matic)): ")
    network = input()
    account_id = ""
    if network == NEAR_SYMBOL.lower() or config.get_network() == NEAR_SYMBOL.lower():
        wallet = Wallet(config.get_keypair_near_path())
        printd("Account ID (ex: bxdoan.near): ")
        account_id = input()
    else:
        wallet = Wallet(config.get_keypair_path())

    if wallet.is_wallet_exited():
        printd("Wallet existed, do you want to override (y/n): ")
        is_override = input()
        is_override = helper.normalize_to_bool(is_override)
        if is_override is not True:
            quit()

    printd("Private key (default for new wallet): ")
    private_key = input()

    printd("Password (len >= 6): ")
    password = getpass("")

    while len(password) < 6:
        printd("Password (len >= 6): ")
        password = getpass("")

    printd("Confirm password: ")
    confirm_password = getpass("")

    if confirm_password != password:
        printd("Password mismatch")
    elif network == NEAR_SYMBOL.lower() or config.get_network() == NEAR_SYMBOL.lower():
        new_address = NearWallet(
            keypair_path=config.get_keypair_near_path(),
            account_id=account_id,
            private_key=private_key,
        ).create_wallet(password)
        printd("Create new wallet with address " + str(new_address))
    else:
        new_address = wallet.create_wallet(private_key, password)
        printd("Create new wallet with address " + new_address)

