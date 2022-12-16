import os
import json

from pywallet.config import Config
from pywallet import constants


def set_up():
    if not os.path.exists(constants.WALLET_PATH):
        os.makedirs(constants.WALLET_PATH)

        config_sample_path = os.path.join(constants.HOME_DIR, 'config.sample.json')
        with open(config_sample_path, "r") as cs:
            config_sample = json.load(cs)
            config_sample.update({"keypair_path": f"{constants.WALLET_LIST_PATH}/id.json"})
            config_sample.update({"keypair_near_path": f"{constants.WALLET_LIST_PATH}/default.near.json"})

            config_path = os.path.join(constants.WALLET_PATH, constants.JSON_CONF)
            with open(config_path, "w+") as f:
                f.write(json.dumps(config_sample, indent = 4))

    if not os.path.exists(constants.WALLET_LIST_PATH):
        os.makedirs(constants.WALLET_LIST_PATH)

    Config().diff_and_update()


set_up()
