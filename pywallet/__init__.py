import os
import json
from pywallet.constants import JSON_CONF, DEFAULT_CONFIG, WALLET_PATH, WALLET_LIST_PATH


def set_up():
    if not os.path.exists(WALLET_PATH):
        os.makedirs(WALLET_PATH)

        config_path = os.path.join(WALLET_PATH, JSON_CONF)
        with open(config_path, "w+") as f:
            f.write(json.dumps(DEFAULT_CONFIG, indent = 4))

    if not os.path.exists(WALLET_LIST_PATH):
        os.makedirs(WALLET_LIST_PATH)


set_up()
