from pywallet.constants import PrintType
from pywallet.print import Print


def test_print_error():
    Print(type_p=PrintType.ERROR)._out(message="test error message")

    assert 1 == 1


def test_print_success():
    Print(type_p=PrintType.SUCCESS)._out(message="test error message")

    assert 1 == 1


def test_print_info():
    Print(type_p=PrintType.INFO)._out(message="test error message")

    assert 1 == 1


def test_print_warning():
    Print(type_p=PrintType.WARNING)._out(title='Using Default', message="test error message")

    assert 1 == 1
