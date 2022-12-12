#! /usr/bin/env python3
import click

from pywallet import helper
from pywallet.config import Config
from pywallet.constants import PrintType
from pywallet.token import TokenSearch
from pywallet.wallet import Wallet
from pywallet.print import printd



@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-n', '--network', 'network', help="Network (default for eth)", default='', show_default=True)
def get_token(network: str) -> None:
    """
    Get token\n
    Usage: token get
    """
    config_data = Config().get_config()
    if not network:
        network = config_data["network"]

    list_token_address = Config().get_coin_list(network)
    list_tokens = TokenSearch(
        network=network,
    ).search_by_address(list_token_address=list_token_address)
    longest = helper.get_length_of_longest_string_value_in_list_of_dict(list_tokens, key="symbol")
    for t in list_tokens:
        printd(msg=f"Address: {t['address']} Symbol: {t['symbol']:>{longest}} Name: {t['name']}")


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument("coin_address", type=str)
@click.option('-n', '--network', 'network', help="Network (default for eth)", default='', show_default=True)
def set_token(coin_address : str, network : str) -> None:
    """
    Set token\n
    Usage: token set <coin_address> -n <network>
    """
    config_data = Config().get_config()
    if not network:
        network = config_data["network"]

    Config().set_coin_address(coin_address=coin_address, network=network)


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument("coin_address", type=str)
@click.option('-n', '--network', 'network', help="Network (default for eth)", default='', show_default=True)
def del_token(coin_address : str, network : str) -> None:
    """
    Del token\n
    Usage: token del <coin_address> -n <network>
    """
    config_data = Config().get_config()
    if not network:
        network = config_data["network"]

    Config().del_coin_address(coin_address=coin_address, network=network)


@click.group()
def token_command():
    """Config token address for wallet"""
    pass


token_command.add_command(get_token, "get")
token_command.add_command(set_token, "set")
token_command.add_command(del_token, "del")
