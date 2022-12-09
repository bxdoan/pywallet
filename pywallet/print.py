#! /usr/bin/env python3
from pywallet import constants
from pywallet.constants import PrintType


class Print(object):

    def __init__(self, type_p: str = PrintType.INFO, **kwargs) -> None:
        self.type_p = type_p

    def _get_color_print(self):
        if self.type_p == PrintType.ERROR:
            return constants.CRED
        elif self.type_p == PrintType.INFO:
            return constants.CCYAN
        elif self.type_p == PrintType.SUCCESS:
            return constants.GRN
        elif self.type_p == PrintType.WARNING:
            return constants.CYELLOW
        else:
            return constants.WHITE

    def _out(self, title: str = '', message: str = '') -> None:
        color_print = self._get_color_print()
        print_fmt = f'{color_print}{self.type_p.upper()}{constants.CEND} - '
        if title:
            print_fmt += f'{title} - '

        print(print_fmt, end='')
        print(message, end="\n", flush=True)


def printd(msg='', type_p=None) -> None:
    if type_p:
        Print(type_p=type_p)._out(message=msg)
    else:
        Print()._out(message=msg)
