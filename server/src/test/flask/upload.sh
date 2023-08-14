#!/bin/bash


curl -X POST -H "Content-Type: application/json" http://localhost:8000/upload -d '{ "serverId": 1, "targetId": 1, "delay": 121.25, "loss": 0.11, "time": "2022-01-11" }'
