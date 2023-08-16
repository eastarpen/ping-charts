#!/bin/bash

set -e

green_output() {
    echo -e "\033[32m$1\033[0m"
}

red_output() {
    echo -e "\033[31m$1\033[0m"
}

file_not_exist() {
    if [ -e "$1" ]; then
        red_output "File '$1' exist."
        return 1;
    fi
}

if [[ $EUID -ne 0 ]]; then
    red_output "This script must be run with root permission."
    exit 1
fi

mkdir -p /opt/ping-charts && cd /opt/ping-charts

FILES=(
    '/opt/ping-charts/ping-charts-client' # make sure this file is executable
    '/opt/ping-charts/client.yaml'
    '/etc/systemd/system/pingChartsClient.service'
    '/etc/systemd/system/pingChartsClient.timer'
)
URLS=(
    'https://github.com/eastarpen/ping-charts/releases/download/v1.1.0/ping-charts-client-go-v1.1.0'
    'https://raw.githubusercontent.com/eastarpen/ping-charts/master/doc/templates/client.yaml'
    'https://raw.githubusercontent.com/eastarpen/ping-charts/master/doc/templates/pingChartsClient.service'
    'https://raw.githubusercontent.com/eastarpen/ping-charts/master/doc/templates/pingChartsClient.timer'
)

for index in "${!FILES[@]}"; do
    file=${FILES[$index]}
    if  file_not_exist "$file" ; then
        wget -O "$file" "${URLS[$index]}"
    fi
done

chmod +x "${FILES[0]}"

green_output 'Ping Charts client has been downloaded.'
green_output 'After configuration, run the following commands:'
green_output 'sudo systemctl start pingChartsClient.timer'
green_output 'sudo systemctl enable pingChartsClient.timer'
