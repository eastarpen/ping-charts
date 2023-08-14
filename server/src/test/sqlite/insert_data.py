#!/bin/env python3

import datetime
import random
import sys

path = "../../" # src directory

sys.path.append(path)


from lib import database as db

def insert_large(start):
    count = 2484000
    ls = []
    for _ in range(count):
        start = start + datetime.timedelta(seconds=20)
        serverId = random.randint(1, 10)
        targetId = random.randint(1, 3)
        delay    = random.uniform(20, 200)
        loss     = random.uniform(0, 0.33)
        ls.append(db.entry(serverId, targetId, start, loss, delay))
    db.insert_entries(ls)

if __name__ == "__main__":
    path = path + 'data'
    db.init_db(path=path)
    timestamp = datetime.datetime(2022,1,1,0,0,0)
    insert_large(timestamp)
