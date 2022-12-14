# Python Wallet - PyWallet

[![Build Status](https://github.com/bxdoan/pywallet/actions/workflows/main.yml/badge.svg)](https://github.com/bxdoan/pywallet/actions/workflows/main.yml/badge.svg)


PyWallet is python script encrypt your private key. Unlike normal extension wallet, PyWallet can't connect to browser, 
so it can't be hack

PyWallet support network `eth`, `matic` and `near`.


![alt text](https://raw.githubusercontent.com/bxdoan/pywallet/main/assets/preview.png)

## Set up
1. Install package
```sh
wget -O setup.sh https://raw.githubusercontent.com/bxdoan/pywallet/main/script/setup.sh && chmod +x setup.sh && ./setup.sh
```

or clone this repo and run
```sh
pip3 install -r requirements.txt
```
or using pipenv
```sh
pipenv sync
```

2. Execute mod for wallet.py
```sh
chmod +x ./run.py
```

## Usage
1. Run app
```sh
./run.sh
```

or run in python

```sh
./pywallet.py
```
NOTE:
By default, we use RPC from alchemy service to get balance and transaction. If you want to use your own url link,
you can create it from [alchemy](https://raw.githubusercontent.com/bxdoan/pywallet/main/docs/alchemy.md) and add it to config.json
```shell
config set --url "https://eth-mainnet.g.alchemy.com/v2/qzq9rBJLZpygokkr-JVb0J26UGF6yGKl" --keypair-file "path/to/your/keypair/file"
```

If you not have wallet, it will create new wallet and save to file *.json by command
```sh
./pywallet.py create
```
You can change url and keypair_path for your own config in `~/.pywallet/config.json` and view your wallet 
keypair in `~/.pywallet/wallet/id.json`

2. Get wallet address
```sh
./pywallet.py address
```

3. Transfer Token
```sh
./pywallet.py transfer <reicever> <amount>

./pywallet.py transfer <reicever> <amount> -t <token_address>
```

4. Get balance
```sh
./pywallet.py balance
```

5. Search TOKEN address
```sh
./pywallet.py search <key_search>
./pywallet.py search AAVE
./pywallet.py search DOGE
```

## Test 
1. Run test 
```sh 
pytest -s
```

or 
```sh
./quicktest.sh
```

NOTE: you can read more in [Usage.md](https://raw.githubusercontent.com/bxdoan/pywallet/main/docs/Usage.md)

## Contact
[Telegram](https://t.me/bxdoan)

[Email](mailto:hi@bxdoan.com)

## Thanks for use
Buy me a coffee

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://paypal.me/bxdoan)

