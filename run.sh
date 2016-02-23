#!/bin/bash

echo "Starting the queue broker in the background..."
(bin/queue_broker) &
echo "The queue broker has PID: $!"
