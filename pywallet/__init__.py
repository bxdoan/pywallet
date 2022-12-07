import os
import json
from pywallet import constants

default_config = {
    "keypair_path": constants.WALLET_PATH + "/wallet" + "/id.json",
    "url": "https://mainnet.infura.io/v3/9e4bc49c44c34ac7ae3e5c34fe5e1d62"
}


def set_up():
    if not os.path.exists(constants.WALLET_PATH):
        os.makedirs(constants.WALLET_PATH)

        config_path = os.path.join(constants.WALLET_PATH, JSON_CONF)
        with open(config_path, "w+") as f:
            f.write(json.dumps(default_config, indent = 4))

    if not os.path.exists(constants.WALLET_LIST_PATH):
        os.makedirs(constants.WALLET_LIST_PATH)


set_up()
