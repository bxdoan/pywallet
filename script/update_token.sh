#!/bin/bash
SH=$(cd `dirname $BASH_SOURCE` && pwd)  # get SH=executed script's path
PH=$(cd "$SH/.." && pwd)  # get PH=executed script's path, PyWallet folder
RH=$(cd "$PH/.." && pwd)   # get RH=executed script's path, containing folder

EC='\033[0m'    # end coloring
HL='\033[0;33m' # high-lighted color
ER='\033[0;31m' # red color

CM='\033[0;32m' # comment color
GR='\033[0;32m' # green color
WH='\033[0;37m' # white color
DIRECTORY='ethereum-lists'

echo -e "${GR}Updating server and installing other necessary things..${EC}"
echo "======================================================"
sleep 1
sudo apt update && sudo apt upgrade -y
sudo apt install curl git -y



echo -e "${GR}Clone ethereum-lists..${EC}"
echo "======================================================"
sleep 1
cd $RH
if [[ -d "$RH/$DIRECTORY" ]]; then
    echo "$DIRECTORY exists"
    cd "$RH/$DIRECTORY"
    git pull
    # shellcheck disable=SC2103
    cd $RH
else
    echo "$DIRECTORY does NOT exists"
    git clone https://github.com/MyEtherWallet/ethereum-lists
fi

# shellcheck disable=SC2016
echo -e "${GR}Copy tokens..${EC}"
echo "======================================================"
sleep 1
cd $RH
from="$RH/$DIRECTORY/src/tokens/"
to="$PH/tokens/"
echo "copy from: $from to: $to"
cp -r "$RH/$DIRECTORY/src/tokens/" $PH/tokens

