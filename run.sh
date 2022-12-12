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
░#####    ░#   #  ░#    #    ░##    ░#       ░#       ░######   ░#######
░#    #    ░# #   ░#    #   ░#  #   ░#       ░#       ░#           ░#
░#    #     ░#    ░#    #  ░#    #  ░#       ░#       ░#           ░#
░#####      ░#    ░# ## #  ░######  ░#       ░#       ░######      ░#
░#          ░#    ░##  ##  ░#    #  ░#       ░#       ░#           ░#
░#          ░#    ░##  ##  ░#    #  ░#       ░#       ░#           ░#
░#          ░#    ░#    #  ░#    #  ░######  ░######  ░######      ░#
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
[4] network      Config network for wallet
[5] create       Create new keypair
[6] search       Search token information by search key
[7] transfer     Transfer for wallet
[8] token        Config token address for wallet
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
	printf "${GR}\nWhat do you want get network or set network ?\n
[1] get  Get network config
[2] set  Set network config
[0] exit Exit
${EC}
"
	read -p $'\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Choose an option: \e[1;92m' optionconfig
	if [[ $optionconfig == 1 || $optionconfig == 01 ]]; then
    printf "\n\e[1;92m Please wait ...\n\n\e[1;92m"
    ./pywallet.py network get
    script
  elif [[ $optionconfig == 2 || $optionconfig == 02 ]]; then
    printf "\nEnter network (None for using eth)...\n"
	  read -p $'\n\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Enter network: \e[1;92m' network
    python3 ./pywallet.py network set --network $network
    script
  else
    script
  fi

elif [[ $option == 5 || $option == 05 ]]; then
	printf "\n\e[1;92m Please wait ...\n\n\e[1;92m"
	python3 ./pywallet.py create
	script

elif [[ $option == 6 || $option == 06 ]]; then
	printf "\n\nEnter search key ...\n"
	read -p $'\n\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Enter search key: \e[1;92m' key_search

	printf "\n\nEnter network (None is eth) ...\n"
	read -p $'\n\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Enter network: \e[1;92m' network

	if [[ $network == "" ]]; then
    network="eth"
  fi
	python3 ./pywallet.py search "$key_search" -n $network
	script

elif [[ $option == 7|| $option == 07 ]]; then
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

elif [[ $option == 8 || $option == 08 ]]; then
	printf "${GR}\nWhat do you want get token address or set token address ?\n
[1] get  Get token address config
[2] set  Set token address config
[3] del  Delete token address config
[0] exit Exit
${EC}
"
	read -p $'\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Choose an option: \e[1;92m' optionconfig
	if [[ $optionconfig == 1 || $optionconfig == 01 ]]; then
    printf "\n\e[1;92m Please wait ...\n\n\e[1;92m"
    printf "\nEnter network (None for using your default config)...\n"
	  read -p $'\n\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Enter network: \e[1;92m' network
	  if [[ $network == "" ]]; then
     ./pywallet.py token get
    else
     ./pywallet.py token get -n $network
    fi
    script
  elif [[ $optionconfig == 2 || $optionconfig == 02 ]]; then
    printf "\nEnter address...\n"
	  read -p $'\n\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Enter address: \e[1;92m' address
    printf "\nEnter network (None for using your default config)...\n"
	  read -p $'\n\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Enter network: \e[1;92m' network
	  if [[ $network == "" ]]; then
     ./pywallet.py token set $address
    else
      ./pywallet.py token set $address --network $network
    fi
    script
  elif [[ $optionconfig == 3 || $optionconfig == 03 ]]; then
    printf "\nEnter address ...\n"
	  read -p $'\n\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Enter address: \e[1;92m' address
	  printf "\nEnter network (None for using your default config)...\n"
	  read -p $'\n\n\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m]\e[1;93m Enter network: \e[1;92m' network
	  if [[ $network == "" ]]; then
	    ./pywallet.py token del $address
    else
      ./pywallet.py token del $address --network $network
    fi
    script
  else
    script
  fi

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