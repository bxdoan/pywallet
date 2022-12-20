from pywallet import helper


def test_encrypt_decrypt():
    # prepare
    secret = "123456"
    text = "hello world"
    # encrypt
    encrypted = helper.PyWalletCry(secret).encrypt(text)

    # decrypt
    decrypted = helper.PyWalletCry(secret).decrypt(encrypted)
    assert decrypted == text
