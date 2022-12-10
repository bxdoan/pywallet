import os
import json

from pywallet.config import Config
from pywallet.constants import JSON_CONF, WALLET_PATH, WALLET_LIST_PATH, HOME_DIR


def set_up():
    if not os.path.exists(WALLET_PATH):
        os.makedirs(WALLET_PATH)

        config_sample_path = os.path.join(HOME_DIR, 'config.sample.json')
        with open(config_sample_path, "r") as cs:
            config_sample = json.load(cs)

            config_path = os.path.join(WALLET_PATH, JSON_CONF)
            with open(config_path, "w+") as f:
                f.write(json.dumps(config_sample, indent = 4))

    if not os.path.exists(WALLET_LIST_PATH):
        os.makedirs(WALLET_LIST_PATH)

    Config().diff_and_update()


set_up()
