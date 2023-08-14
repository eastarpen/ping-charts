#!/bin/bash

set -e

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run with root permission."
    exit 1
fi

mkdir -p /opt/ping-charts && cd /opt/ping-charts

wget -O /opt/ping-charts/ping-charts-client 'https://github.com/eastarpen/ping-charts/releases/download/v1.0.0.0/ping-charts-client'
wget -O /opt/ping-charts/client.yaml 'https://raw.githubusercontent.com/eastarpen/ping-charts/master/doc/templates/client.yaml'
wget -O '/etc/systemd/system/pingChartsClient.service' 'https://raw.githubusercontent.com/eastarpen/ping-charts/master/doc/templates/pingChartsClient.service'
wget -O '/etc/systemd/system/pingChartsClient.timer' 'https://raw.githubusercontent.com/eastarpen/ping-charts/master/doc/templates/pingChartsClient.timer'

echo 'Ping Charts client has been downloaded.'
echo 'After configuration, run the following commands:'
echo 'sudo systemctl start pingChartsClient.timer'
echo 'sudo systemctl enable pingChartsClient.timer'
