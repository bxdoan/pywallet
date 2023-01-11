
from itertools import cycle
from random import randint


class PyWalletCry:
    def __init__(self, secret_key : str = ''):
        self.secret_key = secret_key

    def encrypt(self, text):
        """
        This function will encrypt text to base58 string
        :return
            - base64 string
            - False if text is blank/null
        """
        if not text:
            return False
        addition_char = randint(0, 0x100)
        if len(text) > len(self.secret_key):
            pwd_iterable = cycle(self.secret_key)
        else:
            pwd_iterable = self.secret_key
        ret = [chr(((ord(i) ^ ord(j)) + addition_char) % 0x100) for i, j in zip(text, pwd_iterable)]
        return "".join(reversed(ret)) + chr(addition_char)

    def decrypt(self, text):
        """
        This function is used to decrypt text purpose
        """
        if not text:
            return False
        addition_char = ord(text[-1])
        if len(text) > len(self.secret_key):
            pwd_iterable = cycle(self.secret_key)
        else:
            pwd_iterable = self.secret_key
        ret = [chr((((ord(i) - addition_char) + 0x100) % 0x100) ^ ord(j)) for i, j in
               zip(reversed(text[:-1]), pwd_iterable)]
        return "".join(ret)


def encrypt_(password : str, encrypted_key : str) -> str:
    return PyWalletCry(password).encrypt(encrypted_key)


def decrypt_(password : str, encrypted_key : str) -> str:
    return PyWalletCry(password).decrypt(encrypted_key)
