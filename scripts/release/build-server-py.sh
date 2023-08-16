#!/bin/bash


# working directory should be scripts/release

set -e

cd ../../server/src/ || exit
pip install -r ../requirements.txt


# This will generate file './ping-charts-server'
source build.source

mv ping-charts-server "../../dist/ping-charts-server-python-${GITHUB_REF_NAME}"
