from flask import Flask, render_template, request
import json
import click
import os
import logging

from lib import database as db
from lib import utils, respentity

targets, clients = None, None
targetList = None

app = Flask(__name__)


@app.route("/data", methods=["GET"])
def getChartData():
    min = request.args.get("min")

    if not min or not min.isdigit():
        logging.info("request param min error")
        return "", 500

    time = utils.calculate_time(int(min))
    rows = []
    for client_dict in clients:
        clientDataList = []
        for target_dict in targets:
            targetId, clientId = target_dict["id"], client_dict["id"]
            entries = db.query_entries(time, clientId, targetId)
            clientDataList.append(utils.dbentries_to_chartData(entries))
        rows.append(
            respentity.row(client_dict["name"], client_dict["label"], clientDataList)
        )

    resp = respentity.response(targetList, rows)
    resp_json = json.dumps(resp.__dict__, default=lambda o: o.__dict__)
    return resp_json


def check_reqeust(d: dict):
    # check keys
    if "clientId" not in d or "name" not in d or "passw" not in d or "data" not in d:
        logging.info("json data format error")
        return None
    for client_dict in clients:
        # check client name and password and id
        if client_dict["id"] != d["clientId"]:
            continue
        if client_dict["name"] != d["name"] or client_dict["pass"] != d["passw"]:
            logging.info("auth failed")
            return None
        res = []
        for tar in targets:
            entry = None
            for data in d["data"]:
                try:
                    if tar["id"] != data["id"] or tar["name"] != data["name"]:
                        continue
                    entry = db.entry(
                        d["clientId"],
                        tar["id"],
                        data["time"],
                        data["loss"],
                        data["delay"],
                    )
                except KeyError:
                    logging.info("data format error")
                    return None
                break
            if entry:
                res.append(entry)
        return res


@app.route("/upload", methods=["POST"])
def uploadData():
    data = request.get_json()
    data = check_reqeust(data)
    if not data:
        return "err", 400
    try:
        db.insert_entries(data)
    except Exception:
        logging.error('insert error')
        return "err", 500
    return ""


@app.get("/")
def root():
    return render_template("index.html")


@click.command()
@click.option(
    "--config",
    "-c",
    default="./server.yaml",
    help="YAML config file path, default './server.yaml'",
)
@click.option(
    "--data",
    "-d",
    default="./data",
    help="Direcotry to store data, './data/' defaulted",
)
@click.option(
    "--port",
    "-p",
    default=8000,
    help="client port, 8000 defaulted",
)
@click.option(
    "--local",
    "-l",
    help="Listen 127.0.0.1 only",
    is_flag=True,
)
@click.option(
    "--debug",
    help="Set Log level to DEBUG",
    is_flag=True,
)
def server(
    config: str,
    data: str,
    port: int,
    local: bool,
    debug: bool,
):
    """Ping Charts client"""
    # init logging
    logging_level = logging.DEBUG if debug else logging.INFO
    utils.init_logging(logging_level)

    if not os.path.exists(config):
        logging.error("config file not exist")
        return

    global targets, clients, targetList, app
    targets, clients = utils.load_config(config)

    targetList = [e["name"] for e in targets]

    host = "127.0.0.1" if local else "0.0.0.0"

    db.init_db(path=data, createDir=True)

    logging.debug(
        f"listen on {host}:{port}, logging level: {logging_level}, data dir: {data}"
    )

    app.run(
        port=port,
        host=host,
    )


if __name__ == "__main__":
    server()
