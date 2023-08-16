#!/bin/bash


# working directory should be scripts/release

set -e

cd ../../client/src/ || exit
pip install -r ../requirements.txt


# This will generate file './ping-charts-client'
source build.source

mv ping-charts-client "../../dist/ping-charts-client-python-${GITHUB_REF_NAME}"
