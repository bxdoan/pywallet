#! /usr/bin/env python3
import os
import json
from pywallet.constants import JSON_CONF, WALLET_PATH, PrintType, DEFAULT_CONFIG, NETWORK_DEFAULT
from pywallet.print import printd


class Config(object):
    def __init__(self):
        self.config = None
        self._get_config()

    def _get_config(self) -> dict:
        config_path = os.path.join(WALLET_PATH, JSON_CONF)
        with open(config_path, "r") as f:
            self.config = json.load(f)
        return self.config

    def get_config(self):
        return self.config

    def set_config(self, url: str = None, keypair_file: str = None, network: str = None) -> bool:
        config = self.config
        if url is not None:
            printd(msg="URL: " + url, type_p=PrintType.SUCCESS)
            config["url"][network] = url
        if network is not None:
            printd(msg="Network: " + network, type_p=PrintType.SUCCESS)
            config["network"] = network
        if keypair_file is not None:
            printd(msg="Keypair file: " + keypair_file, type_p=PrintType.SUCCESS)
            config["keypair_path"] = keypair_file

        config_path = os.path.join(WALLET_PATH, JSON_CONF)
        with open(config_path, "w+") as f:
            f.write(json.dumps(config, indent = 4))
        printd("Config updated", type_p=PrintType.SUCCESS)
        return True

    def create_default_config(self, path: str) -> None:
        with open(path, "w+") as f:
            f.write(json.dumps(DEFAULT_CONFIG, indent = 4))

    def check_config_exited(self) -> None:
        config_path = os.path.join(WALLET_PATH, JSON_CONF)
        if not os.path.isfile(config_path):
            self.create_default_config(config_path)

    def is_wallet_exited(self) -> bool:
        config_path = os.path.join(self.config["keypair_path"])
        if not os.path.isfile(config_path):
            False
        else:
            True

    def get_keypair_path(self) -> str:
        return self.config["keypair_path"]

    def get_url(self, network : str = None) -> str:
        if not network:
            network = self.config['network']
        return self.config["url"][network]

    def get_network(self) -> str:
        return self.config['network']

    def print_config(self) -> None:
        keypair_path = self.config["keypair_path"]
        url = self.config["url"]
        printd(msg="URL: " + url, type_p=PrintType.SUCCESS)
        printd(msg="Keypair Path" + keypair_path, type_p=PrintType.SUCCESS)
