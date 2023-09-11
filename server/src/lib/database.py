import sqlite3
import os
import math
import logging

from .utils import calculate_timestamp

db_con, db_path = None, None

MAX_ENTRIES = 250
TABLE_NAME = "pingdata"
CREATE_TABLE_SQL = """CREATE TABLE %s (
                      id INTEGER PRIMARY KEY,
                      clientId INTEGER NOT NULL,
                      targetId INTEGER NOT NULL,
                      time INTEGER NOT NULL,
                      loss FLOAT NOT NULL,
                      delay FLOAT NOT NULL);""" % (
    TABLE_NAME
)

INSERT_ENTRY_SQL = """ INSERT INTO %s
                       ('clientId', 'targetId', 'time', 'loss', 'delay')
                       VALUES(?,?,?,?,?);""" % (
    TABLE_NAME
)

QUERY_ENTRY_SQL = """SELECT clientId, targetId, time, loss, delay FROM %s
                     WHERE time > ? AND clientId = ? AND targetId = ?;""" % (
    TABLE_NAME
)

DELETE_OLD_DATA_SQL = """DELETE FROM %s where time < ?;""" % (TABLE_NAME)


class entry:
    def __init__(
        self,
        clientId: int,
        targetId: int,
        time: int,
        loss: float,
        delay: float,
    ) -> None:
        self.clientId = clientId
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
                logging.info("Create table [%s]" % TABLE_NAME)
                con.execute(CREATE_TABLE_SQL)

    except sqlite3.Error:
        logging.error("Error while init db.")


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
            data = [(e.clientId, e.targetId, e.time, e.loss, e.delay) for e in entries]
            con.executemany(INSERT_ENTRY_SQL, data)
    except sqlite3.Error:
        logging.error("Error while insert entries.")


def insert_entry(
    entry: entry,
):
    insert_entries([entry])


def query_entries(timestamp: float, clientId: int, targetId: int):
    res = []
    try:
        with get_connection() as con:
            records = con.execute(QUERY_ENTRY_SQL, (timestamp, clientId, targetId)).fetchall()
            step = math.ceil(len(records) / MAX_ENTRIES)
            res = [entry(*r) for idx, r in enumerate(records) if idx % step == 0]
    except sqlite3.Error:
        logging.error("Error while query entries.")
    return res


def delete_old_data(day = 7):
    time = calculate_timestamp(60 * 24 * day)  # mins
    try:
        with get_connection() as con:
            con.execute(DELETE_OLD_DATA_SQL, (time,))
    except sqlite3.Error:
        logging.error("Error while delete old data.")
