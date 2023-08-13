#!/bin/env python3

from datetime import datetime
import sys

lib_path = "/home/eastarpen/dev/ping-long-time/ping-charts-flask/src"
path = "/home/eastarpen/dev/ping-long-time/ping-charts-flask/src/data"

sys.path.append(lib_path)

from lib import database as db

if __name__ == "__main__":
    db.init_db(path=path)
    timestamp = datetime(2023,1,1,0,0,0)

    res = db.query_entries(timestamp,1,1, )
    print(res)
