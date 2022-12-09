#!/usr/bin/env bash

SH=$(cd `dirname $BASH_SOURCE` && pwd)  # get SH=executed script's path

EC='\033[0m'    # end coloring
HL='\033[0;33m' # high-lighted color
ER='\033[0;31m' # red color

CM='\033[0;32m' # comment color
GR='\033[0;32m' # green color
WH='\033[0;37m' # white color
DIRECTORY='pywallet'

echo -e "${GR}Updating server and installing other necessary things..${EC}"
echo -e "${GR}======================================================${EC}"
sudo apt update && sudo apt upgrade -y
sudo apt install curl git python3-pip -y
echo

echo -e "${GR}Clone PyWallet..${EC}"
echo -e "${GR}======================================================${EC}"
git clone https://github.com/bxdoan/pywallet $DIRECTORY
cd "$SH/$DIRECTORY"

echo -e "${GR}Install package..${EC}"
echo -e "${GR}======================================================${EC}"
pip3 install -r requirements.txt


printf "
    ${GR}PyWallet: Micro wallet by bxdoan${EC}
    ${GR}Email: hi@bxdoan.com${EC}

    ${GR}USAGE${EC}

1. Create your wallet
    ./pywallet.py create

2. Get your wallet address
    ./pywallet.py address

3. Get your wallet balance
    ./pywallet.py balance

4. Send your wallet balance
    ./pywallet.py transfer <reicever> <amount>

    ./pywallet.py transfer <reicever> <amount> -t <token_address>

    ./pywallet.py transfer 0x123 1 -t 0x321

5. Search TOKEN address
    ./pywallet.py search <key_search>
    ./pywallet.py search AAVE
    ./pywallet.py search DOGE

"
