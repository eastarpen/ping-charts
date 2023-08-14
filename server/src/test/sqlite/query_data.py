#!/bin/env python3

from datetime import datetime
import sys

lib_path = "../../" # src directory

sys.path.append(lib_path)

from lib import database as db

if __name__ == "__main__":
    data_path = lib_path + 'data'
    db.init_db(path=data_path)
    timestamp = datetime(2023,1,1,0,0,0)

    res = db.query_entries(timestamp,1,1, )
    print(res)
