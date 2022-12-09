#! /usr/bin/env python3
import click
from pywallet.constants import PrintType
from pywallet.token import TokenSearch
from pywallet.print import printd


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument("search_key", type=str)
def search_token(search_key: str) -> None:
    """
    Search token information by search key\n
    Usage: search <search_key>
    """
    list_tokens = TokenSearch(search_key=search_key).search()
    if len(list_tokens) == 0:
        printd(msg="Not found", type_p=PrintType.ERROR)
        quit()
    printd(msg=f"Found {len(list_tokens)} results", type_p=PrintType.SUCCESS)

    for t in list_tokens:
        printd(msg=f"Name: {t['name']}, Symbol: {t['symbol']}, Address: {t['address']}")
