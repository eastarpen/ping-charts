#!/bin/env python3

import sys

path = "/home/eastarpen/dev/ping-long-time/server-backend/src"
sys.path.append(path)

from lib import database as db


if __name__ == "__main__":
    path = "/home/eastarpen/dev/ping-long-time/server-backend/src" + "/data"
    db.init_db(path=path)
    db.delete_old_data()
