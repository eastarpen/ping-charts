#!/bin/bash

set -e

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run with root permission."
    exit 1
fi

mkdir -p /opt/ping-charts && cd /opt/ping-charts

wget -O /opt/ping-charts/ping-charts-server 'server url'
wget -O /opt/ping-charts/server.yaml 'server config url'
wget -O '/etc/systemd/system/pingChartsServer.service' 'client service url'

echo 'Ping Charts server has been downloaded.'
echo 'After configure, run the following commands:'
echo 'sudo systemctl enable pingChartsServer'
echo 'sudo systemctl start pingChartsServer'
