#!/bin/bash


# working directory should be scripts/release

set -e

cd ../../client-go/ || exit

# This will generate file './ping-charts-client'
go build

mv client-go "../dist/ping-charts-client-go-${GITHUB_REF_NAME}"
