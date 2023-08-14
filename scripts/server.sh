#!/bin/bash

set -e

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run with root permission."
    exit 1
fi

mkdir -p /opt/ping-charts && cd /opt/ping-charts

wget -O /opt/ping-charts/ping-charts-server 'https://github.com/eastarpen/ping-charts/releases/download/v1.0.0.0/ping-charts-server'
wget -O /opt/ping-charts/server.yaml 'https://raw.githubusercontent.com/eastarpen/ping-charts/master/doc/templates/server.yaml'
wget -O '/etc/systemd/system/pingChartsServer.service' 'https://raw.githubusercontent.com/eastarpen/ping-charts/master/doc/templates/pingChartsServer.service'

echo 'Ping Charts server has been downloaded.'
echo 'After configuration, run the following commands:'
echo 'sudo systemctl enable pingChartsServer'
echo 'sudo systemctl start pingChartsServer'
