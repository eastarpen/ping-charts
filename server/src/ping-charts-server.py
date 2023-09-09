from flask import Flask, render_template, request
import json
import click
import os
import logging

from lib import database as db
from lib import utils, respentity


VERSION = "v1.2.0"

targets, clients = None, None
targetList = None

app = Flask(__name__)


@app.route("/data", methods=["GET"])
def getChartData():
    min = request.args.get("min")

    if not min or not min.isdigit():
        logging.info("Request param min error")
        return "Bad Request", 400

    time = utils.calculate_timestamp(int(min))
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
    if not d or "clientId" not in d or "name" not in d or "passw" not in d or "data" not in d:
        return "Request data format error", 400
    for client_dict in clients:
        # check client name and password and id
        if client_dict["id"] != d["clientId"]:
            continue
        if client_dict["name"] != d["name"] or client_dict["pass"] != d["passw"]:
            return "Auth Error", 403
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
                    break
                except KeyError:
                    return ("Target data format error", 400)
            if entry:
                res.append(entry)
        return res, 200
    return "Client not found", 400


@app.route("/upload", methods=["POST"])
def uploadData():
    dataDict = request.get_json()
    if dataDict:
        name = dataDict.get('name', 'UNKNOW_NAME')
        id = dataDict.get('clientId', 'UNKNOW_ID')
    data, status_code = check_reqeust(dataDict)
    if  status_code != 200:
        logging.info(f"{name} {id} {data}")
        return data, status_code
    try:
        db.insert_entries(data)
    except Exception:
        logging.error(f'{name} {id} Insert error')
        return "Server Error", 500
    return "Success", 200


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
    help="Service port, 8000 defaulted",
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
@click.option(
    "--version",
    help="Print version and exit",
    default=False,
    is_flag=True,
)
def server(
    config: str,
    data: str,
    port: int,
    local: bool,
    debug: bool,
    version: bool,
):
    """Ping Charts server.\nA simple tool to visualize vps latency based on TCP."""
    if version:
        print("Ping Charts Server-py ", VERSION)
        return
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
