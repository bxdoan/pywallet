#! /usr/bin/env python3
import os
import json

from pywallet import helper
from pywallet import constants
from pywallet.print import pd


class Config(object):
    def __init__(self):
        self.config = None
        self._get_config()

    def _get_config(self) -> dict:
        config_path = os.path.join(constants.WALLET_PATH, constants.JSON_CONF)
        with open(config_path, "r") as f:
            self.config = json.load(f)
        return self.config

    def get_config(self):
        return self.config

    def set_config(self, url: str = None, keypair_file: str = None, network: str = None):
        config = self.config
        if url is not None:
            pd(msg="URL: " + url, type_p=constants.PrintType.SUCCESS)
            config["url"][network] = url
        if network is not None:
            pd(msg="Network: " + network, type_p=constants.PrintType.SUCCESS)
            config["network"] = network
        if keypair_file is not None:
            pd(msg="Keypair file: " + keypair_file, type_p=constants.PrintType.SUCCESS)
            config["keypair_path"] = keypair_file
        self._dump_config()

    def set_coin_address(self, coin_address: str, network : str = None) -> None:
        if not network:
            network = self.config['network']
        network_coin_address = self.config["coin_address"][network]
        network_coin_address = helper.check_string_in_list_of_string_and_add_more_if_not_exited(network_coin_address,
                                                                                                coin_address)
        self.config["coin_address"][network] = network_coin_address
        self._dump_config()

    def del_coin_address(self, coin_address: str, network : str = None) -> None:
        if not network:
            network = self.config['network']
        network_coin_address = self.config["coin_address"][network]
        network_coin_address = helper.check_string_in_list_of_string_and_remove_if_exited(network_coin_address,
                                                                                          coin_address)
        self.config["coin_address"][network] = network_coin_address
        self._dump_config()

    def _dump_config(self, json_conf: dict = None) -> None:
        if json_conf is None:
            json_conf = self.config
        config_path = os.path.join(constants.WALLET_PATH, constants.JSON_CONF)
        with open(config_path, "w+") as f:
            f.write(json.dumps(json_conf, indent = 4))

    def create_default_config(self) -> None:
        config_sample_path = os.path.join(constants.HOME_DIR, 'config.sample.json')
        with open(config_sample_path, "r") as cs:
            config_sample = json.load(cs)
            self._dump_config(json_conf=config_sample)

    def diff_and_update(self):
        config_sample_path = os.path.join(constants.HOME_DIR, constants.JSON_CONF_SAMPLE)
        with open(config_sample_path, "r") as cs:
            config_sample = json.load(cs)
            self.config = helper.diff_dict_and_add_more_key(config_sample, self.config)
            self._dump_config()

    def check_config_exited(self) -> None:
        config_path = os.path.join(constants.WALLET_PATH, constants.JSON_CONF)
        if not os.path.isfile(config_path):
            self.create_default_config()

    def is_wallet_exited(self) -> bool:
        config_path = os.path.join(self.config["keypair_path"])
        if not os.path.isfile(config_path):
            return False
        else:
            return True

    def get_keypair_path(self) -> str:
        return self.config["keypair_path"]

    def get_keypair_near_path(self) -> str:
        return self.config["keypair_near_path"]

    def get_url(self, network : str = None) -> str:
        if not network:
            network = self.config['network']
        return self.config["url"][network]

    def get_coin_list(self, network : str = None) -> list:
        if not network:
            network = self.config['network']
        return self.config["coin_address"][network]

    def get_network(self) -> str:
        return self.config['network']

    def print_config(self) -> None:
        keypair_path = self.config["keypair_path"]
        url = self.config["url"]
        pd(msg="URL: " + url, type_p=constants.PrintType.SUCCESS)
        pd(msg="Keypair Path" + keypair_path, type_p=constants.PrintType.SUCCESS)
