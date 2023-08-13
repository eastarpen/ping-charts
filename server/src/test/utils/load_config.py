#!/bin/python3

import sys

lib_path = "/home/eastarpen/dev/ping-long-time/server-backend/src/lib"
path = "/home/eastarpen/dev/ping-long-time/server-backend/src/data"

sys.path.append(lib_path)

config_file = "/home/eastarpen/dev/ping-long-time/server-backend/src/data/config.yaml"

import utils

if __name__ == "__main__":
    targets, servers = utils.load_config(config_file)
    print(targets)
    print(servers)
