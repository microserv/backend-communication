#!/bin/sh
sleep 2
curl -i -H "Content-Type: application/json" -X POST -d "{'service_name':'$SERVICE_NAME'}" http://localhost:9001/register
