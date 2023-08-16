#!/bin/bash


# working directory should be scripts/release

set -e

cd ../../client-go/ || exit

# This will generate file './ping-charts-client'
go build
mv client-go "../dist/ping-charts-client-go-${GITHUB_REF_NAME}"

# static build 
# https://stackoverflow.com/questions/55450061/go-build-with-another-glibc/61812048#61812048
# https://www.reddit.com/r/golang/comments/pi97sp/what_is_the_consequence_of_using_cgo_enabled0/
export CGO_ENABLED=0
go build
mv client-go "../dist/ping-charts-client-go-static-${GITHUB_REF_NAME}"
