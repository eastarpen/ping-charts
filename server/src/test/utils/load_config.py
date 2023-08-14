#!/bin/python3

import sys

path = "../../"

sys.path.append(path)

from lib import utils



if __name__ == "__main__":
    config_file = "../../data/config.yaml"
    targets, servers = utils.load_config(config_file)
    print(targets)
    print(servers)
