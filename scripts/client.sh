#!/bin/bash

set -e

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run with root permission."
    exit 1
fi

mkdir -p /opt/ping-charts && cd /opt/ping-charts

wget -O /opt/ping-charts/ping-charts-client 'client url'
wget -O /opt/ping-charts/client.yaml 'client config url'
wget -O '/etc/systemd/system/pingChartsClient.service' 'client service url'
wget -O '/etc/systemd/system/pingChartsClient.timer' 'client timer url'

echo 'Ping Charts client has been downloaded.'
echo 'After configure, run the following commands:'
echo 'sudo systemctl start pingChartsClient.timer'
echo 'sudo systemctl enable pingChartsClient.timer'
