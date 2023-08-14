import json
import os
import requests
import click
import socket
import time
import statistics
import datetime
import yaml


CONFIG_KEYS = [
    "name",
    "clientId",
    "passw",
    "uploadUrl",
    "targets",
]
TARGET_KEYS = [
    "id",
    "name",
    "port",
    "addr",
]

clientId = None
passw = None
name = None
tars = None


def load_config(config_file: str):
    assert os.path.exists(config_file), "config file not found"

    conf = None

    with open(config_file) as file:
        conf = yaml.safe_load(file)

    # check keys
    for key in CONFIG_KEYS:
        if key not in conf:
            raise Exception("config file missing key: " + key)

    for tar in conf["targets"]:
        for key in TARGET_KEYS:
            if key not in tar:
                raise Exception("target missing key: " + key)
    return (
        conf["clientId"],
        conf["passw"],
        conf["name"],
        conf["uploadUrl"],
        conf["targets"],
    )


def tcping(host, port=80, count=10, timeout=0.5):
    delays = []
    lost_packets = 0

    for _ in range(count):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)

            start_time = time.time()
            sock.connect((host, port))
            end_time = time.time()

            delay = end_time - start_time
            delays.append(delay)

            sock.close()
        except socket.timeout:
            lost_packets += 1

    avg_delay = statistics.mean(delays) * 1000 if delays else 0
    packet_loss = lost_packets / count

    return avg_delay, packet_loss


def send_request(data: dict, upload_url: str):
    json_data = json.dumps(data)
    response = requests.post(
        upload_url, data=json_data, headers={"Content-Type": "application/json"}
    )
    print(response.status_code)


def generate_data(count: int, timeout: float):
    d = {
        "clientId": clientId,
        "passw": passw,
        "name": name,
    }
    data = []
    for tar in tars:
        res = {
            "name": tar["name"],
            "id": tar["id"],
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        delay, loss = tcping(tar["addr"], tar["port"], count, timeout)
        res["delay"] = delay
        res["loss"] = loss
        data.append(res)
    d["data"] = data
    return d


@click.command()
@click.option(
    "--config",
    "-c",
    default="./client.yaml",
    help="yaml config file, default value './client.yaml'",
)
@click.option(
    "--timeout",
    "-t",
    default=0.5,
    help="time that judged as package loss, 0.5s defaulted. The unit is seconds.",
)
@click.option(
    "--package",
    "-p",
    default=10,
    help="how many packages to send in a test, 10 defaulted",
)
def client(config, timeout, package):
    """Ping Charts client."""
    global clientId, passw, name, tars
    clientId, passw, name, upload_url, tars = load_config(config)
    data = generate_data(package, timeout)
    send_request(data, upload_url)


if __name__ == "__main__":
    client()
