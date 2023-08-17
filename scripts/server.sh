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
    '/opt/ping-charts/ping-charts-server' # make sure this file is executable.
    '/opt/ping-charts/server.yaml'
    '/etc/systemd/system/pingChartsServer.service'
)
URLS=(
    'https://github.com/eastarpen/ping-charts/releases/download/v1.1.0/ping-charts-server-python-v1.2.0'
    'https://raw.githubusercontent.com/eastarpen/ping-charts/master/doc/templates/server.yaml'
    'https://raw.githubusercontent.com/eastarpen/ping-charts/master/doc/templates/pingChartsServer.service'
)

for index in "${!FILES[@]}"; do
    file=${FILES[$index]}
    if  file_not_exist "$file" ; then
        wget -O "$file" "${URLS[$index]}"
    fi
done

chmod +x "${FILES[0]}"

green_output 'Ping Charts server has been downloaded.'
green_output 'After configuration, run the following commands:'
green_output 'sudo systemctl start pingChartsServer.service'
green_output 'sudo systemctl enable pingChartsServer.service'
