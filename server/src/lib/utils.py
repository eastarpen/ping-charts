import yaml
import os
import datetime
import logging

from .respentity import chartData


def load_config(path):
    assert os.path.exists(path), "Configuration file does not exist"

    with open(path, "r") as f:
        res = yaml.load(f, Loader=yaml.FullLoader)
        return res["targets"], res["clients"]


def calculate_time(min: int) -> datetime.datetime:
    """
    Ddeprecated.
    Using calculate_timestamp to solve timezone problem.
    """
    return datetime.datetime.now() - datetime.timedelta(minutes=min)

def calculate_timestamp(min: int) -> int:
    return int(
                (datetime.datetime.now() - datetime.timedelta(minutes=min))
                .timestamp()
            )

def dbentries_to_chartData(entries: list) -> chartData:
    if not entries or len(entries) == 0:
        return chartData.empty()

    return chartData(
        [e.delay for e in entries], [e.loss for e in entries], [e.time for e in entries]
    )


def init_logging(level):
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
