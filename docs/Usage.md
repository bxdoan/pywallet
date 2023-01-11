# Usage

## Create your wallet
For the first time you use the wallet, you need to create a new wallet. You
can do this by running the following command:

```shell
./pywallet.py create
```

## Get your wallet address
You can get your wallet address by running the following command:

```shell
./pywallet.py address
```

## Set up network
PyWallet support network `eth`, `matic` and `near`.

1. Set up network

```shell
./pywallet.py network set --network <network>
```

2 Get default network


```shell
./pywallet.py network get
```

## Get your wallet balance
You can get your wallet balance by running the following command:

```shell
./pywallet.py balance
```

You can also get your wallet balance for a specific token by running the following command:

```shell

## Send your wallet balance

    ./pywallet.py transfer <reicever> <amount>

    ./pywallet.py transfer <reicever> <amount> -t <token_address>

    ./pywallet.py transfer 0x123 1 -t 0x321

## Search TOKEN address

    ./pywallet.py search <key_search>
    ./pywallet.py search AAVE
    ./pywallet.py search DOGE