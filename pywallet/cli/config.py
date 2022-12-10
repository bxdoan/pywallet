#! /usr/bin/env python3
import click
from pywallet.config import Config
from pywallet.constants import NETWORK_DEFAULT
from pywallet.print import printd

config = Config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-n', '--network', 'network', help="Network (default for eth)", default='', show_default=True)
def get_config(network: str) -> None:
    """
    Get config\n
    Usage: config get
    """
    config_data = config.get_config()
    if not network:
        network = config_data["network"]
    printd(msg="Network: " + network)
    printd(msg="URL: " + config_data["url"][network])
    printd(msg="Keypair Path: " + config_data["keypair_path"])


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-u', '--url', 'url', help="RPC URL")
@click.option('-k', '--keypair-file', 'keypair_file', help="Keypair file name")
def set_config(url: str, keypair_file: str, network: str) -> None:
    """
    Set config\n
    Usage: config set -u <url> -k <keypair_file>
    """
    if url is None and keypair_file is None: 
        with click.Context(set_config) as ctx:
            click.echo(set_config.get_help(ctx))
    else:
        success = config.set_config(url=url, keypair_file=keypair_file)

        if success:
            printd(msg="Config updated")


@click.group()
def config_command():
    """Config for wallet"""
    pass


config_command.add_command(get_config, "get")
config_command.add_command(set_config, "set")
