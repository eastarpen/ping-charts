#!/bin/env python3

import sys

path = "../../" # src directory
sys.path.append(path)

from lib import database as db


if __name__ == "__main__":
    path = path + "data"
    db.init_db(path=path)
    db.delete_old_data()
