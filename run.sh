#!/bin/bash
# This script was coded by @bxdoan
# Please give me credits if you us any codes from here.
# GitHub: https://github.com/bxdoan
# Email: hi@bxdoan.com
EC='\033[0m'    # end coloring
HL='\033[0;33m' # high-lighted color
ER='\033[0;31m' # red color

CM='\033[0;32m' # comment color
GR='\033[0;32m' # green color
WH='\033[0;37m' # white color
clear

banner() {
printf "${GR}
#####    #   #  #    #    ##    #       #       ######   #####
#    #    # #   #    #   #  #   #       #       #          #
#    #     #    #    #  #    #  #       #       #          #
#####      #    # ## #  ######  #       #       ######     #
#          #    ##  ##  #    #  #       #       #          #
#          #    ##  ##  #    #  #       #       #          #
#          #    #    #  #    #  ######  ######  ######     #
   Coded by \e[1;94m@bxdoan\e[1;92m
   Email: hi@bxdoan.com
${EC}
"
}

script() {
printf "${GR}
[1] address      Get your wallet address
[2] balance      Get balance
[3] config       Config for wallet
[4] create       Create new keypair
[5] search       Search token information by search key
[6] transfer     Transfer for wallet
[0] exit         Exit
${EC}
"

read -p $'\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Choose an option: \e[1;93m' option

if [[ $option == 1 || $option == 01 ]]; then
	printf "\n\e[1;92m This process will take a few moments ...\n\n\e[1;92m"
  ./pywallet.py address
	script

elif [[ $option == 2 || $option == 02 ]]; then
	printf "\n\e[1;92m Please wait ...\n\n\e[1;92m"
	./pywallet.py balance
	script

elif [[ $option == 3 || $option == 03 ]]; then
	printf "${GR}\nWhat do you want get config or set config ?\n
[1] get  Get config
[2] set  Set config
[0] exit Exit
${EC}
"
	read -p $'\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Choose an option: \e[1;92m' optionconfig

	if [[ $optionconfig == 1 || $optionconfig == 01 ]]; then
    printf "\n\e[1;92m Please wait ...\n\n\e[1;92m"
    ./pywallet.py config get
    script
  elif [[ $optionconfig == 2 || $optionconfig == 02 ]]; then
    printf "\nEnter url (None for using default)...\n"
	  read -p $'\n\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Enter url: \e[1;92m' url
	  printf "\nEnter keypair path (None for using default) ...\n"
	  read -p $'\n\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Enter keypair path: \e[1;92m' keypair
    printf "\n\e[1;92m Please wait ...\n\n\e[1;92m"

    if [[ $url == "" ]]; then
      python3 ./pywallet.py config set --keypair $keypair
    elif [[ $keypair == "" ]]; then
      python3 ./pywallet.py config set --url $url
    else
      python3 ./pywallet.py config set --url $url --keypair $keypair
    fi
    python3 ./pywallet.py config set
    script
  else
    script
  fi
	script

elif [[ $option == 4 || $option == 04 ]]; then
	printf "\n\e[1;92m Please wait ...\n\n\e[1;92m"
	python3 ./pywallet.py create
	script

elif [[ $option == 5 || $option == 05 ]]; then
	printf "\n\nEnter search key ...\n"
	read -p $'\n\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Enter search key: \e[1;92m' key_search

	printf "\n\nEnter network (None is eth) ...\n"
	read -p $'\n\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Enter network: \e[1;92m' network

	if [[ $network == "" ]]; then
    network="eth"
  fi
	python3 ./pywallet.py search "$key_search" -n $network
	script

elif [[ $option == 6 || $option == 06 ]]; then
	printf "\nEnter receiver address ...\n"
	read -p $'\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Enter address: \e[1;92m' reicever

	printf "\nEnter amount ...\n"
	read -p $'\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Enter amount: \e[1;92m' amount

	printf "\nEnter token address (None is Native token) ...\n"
	read -p $'\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Enter token address: \e[1;92m' token_address

	if [[ $token_address == "" ]]; then
    token_address="Native token"
  fi
	python3 ./pywallet.py transfer "$reicever" "$amount" -t "$token_address"
	script

elif [[ $option == 0 || $option == 00 ]]; then
  exit 0
else
	printf "Command not found!
NOTE: If you get any problem while using this tool than please report to
email: hi@bxdoan.com
github: https://github.com/bxdoan
"
fi
}

banner
script