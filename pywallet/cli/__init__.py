#!/usr/bin/env python3

import click

from pywallet.cli.config import config_command
from pywallet.cli.address import get_address
from pywallet.cli.create import create_wallet
from pywallet.cli.tornado import tornado_command
from pywallet.cli.transfer import transfer_handler
from pywallet.cli.balance import balance_handler

__version__ = "0.1.0"


@click.group()
@click.version_option(version = __version__)
@click.pass_context
def cli(ctx):
    """
    PyWallet: Micro wallet by BXDOAN
    Email: hi@bxdoan.com
    """
    pass


cli.add_command(config_command, "config")
cli.add_command(get_address, "address")
cli.add_command(create_wallet, "create")
cli.add_command(tornado_command, "tornado")
cli.add_command(transfer_handler, "transfer")
cli.add_command(balance_handler, "balance")
