#! /usr/bin/env python3
import click
from pywallet.config import Config
from pywallet.constants import NETWORK_DEFAULT
from pywallet.print import printd

config = Config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
def get_network() -> None:
    """
    Get network\n
    Usage: network get
    """
    config_data = config.get_config()
    network = config_data["network"]
    printd(msg="Network: " + network)


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument("network", type=str)
def set_network(network: str) -> None:
    """
    Set network\n
    Usage: config set -n <network>
    """
    if network is None:
        with click.Context(set_network) as ctx:
            click.echo(set_network.get_help(ctx))
    else:
        config.set_config(network=network)


@click.group()
def network_command():
    """Config network for wallet"""
    pass


network_command.add_command(get_network, "get")
network_command.add_command(set_network, "set")
