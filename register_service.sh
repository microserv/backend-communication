#!/bin/sh
sleep 2
curl -S --retry-max-time 10 --retry 5 --retry-delay 5 -i -H "Content-Type: application/json" -X POST -d '{"service_name":"'"$SERVICE_NAME"'"}' http://localhost:9001/register
