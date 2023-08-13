import sqlite3
import os
import datetime
import math
import logging

from .utils import calculate_time

db_con, db_path = None, None

MAX_ENTRIES = 250
TABLE_NAME = "pingdata"
CREATE_TABLE_SQL = """CREATE TABLE %s (
                      id INTEGER PRIMARY KEY,
                      serverId INTEGER NOT NULL,
                      targetId INTEGER NOT NULL,
                      time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                      loss FLOAT NOT NULL,
                      delay FLOAT NOT NULL);""" % (
    TABLE_NAME
)

INSERT_ENTRY_SQL = """ INSERT INTO %s
                       ('serverId', 'targetId', 'time', 'loss', 'delay')
                       VALUES(?,?,?,?,?);""" % (
    TABLE_NAME
)

QUERY_ENTRY_SQL = """SELECT serverId, targetId, time, loss, delay FROM %s
                     WHERE time > ? AND serverId = ? AND targetId = ?;""" % (
    TABLE_NAME
)

DELETE_OLD_DATA_SQL = """DELETE FROM %s where time < ?;""" % (TABLE_NAME)


class entry:
    def __init__(
        self,
        serverId: int,
        targetId: int,
        time: datetime.datetime,
        loss: float,
        delay: float,
    ) -> None:
        self.serverId = serverId
        self.targetId = targetId
        self.time = time
        self.loss = loss
        self.delay = delay


def init_db(dbname="pingcharts.db", path="./", createDir=False) -> None:
    if createDir:
        os.makedirs(path, exist_ok=True)

    if not os.path.exists(path):
        raise FileNotFoundError("Path does not exist: %s" % path)

    global db_path
    db_path = os.path.join(path, dbname)

    try:
        with get_connection() as con:
            # init tables
            res = con.execute(f"SELECT name FROM sqlite_master WHERE name='{TABLE_NAME}'")
            table_not_exist = res.fetchone() is None

            if table_not_exist:
                logging.info("create table [%s]" % TABLE_NAME)
                con.execute(CREATE_TABLE_SQL)

    except sqlite3.Error as error:
        print("Error while working with SQLite", error)


def get_connection():

    global db_con, db_path

    assert db_path

    if not db_con:
        # https://ricardoanderegg.com/posts/python-sqlite-thread-safety/
        db_con = sqlite3.connect(db_path, check_same_thread=False)
    return db_con


def insert_entries(
    entries: list,
):
    assert entries and len(entries) > 0 and isinstance(entries[0], entry)

    try:
        with get_connection() as con:
            data = [(e.serverId, e.targetId, e.time, e.loss, e.delay) for e in entries]
            con.executemany(INSERT_ENTRY_SQL, data)
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)


def insert_entry(
    entry: entry,
):
    insert_entries([entry])


def query_entries(timestamp: datetime.datetime, serverId: int, targetId: int):
    res = []
    try:
        with get_connection() as con:
            records = con.execute(QUERY_ENTRY_SQL, (timestamp, serverId, targetId)).fetchall()
            step = math.ceil(len(records) / MAX_ENTRIES)
            res = [entry(*r) for idx, r in enumerate(records) if idx % step == 0]
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    return res


def delete_old_data():
    time = calculate_time(60 * 24 * 30)  # mins
    try:
        with get_connection() as con:
            con.execute(DELETE_OLD_DATA_SQL, (time,))
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
