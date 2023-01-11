from pywallet import auth


def test_encrypt_decrypt():
    # prepare
    secret = "123456"
    text = "hello world"
    # encrypt
    encrypted = auth.encrypt_(secret, text)

    # decrypt
    decrypted = auth.decrypt_(secret, encrypted)
    assert decrypted == text
