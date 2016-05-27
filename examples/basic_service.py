"""
This examples assumes that you already have a node listening on port 9001
A new node is started by running the following command:

    python node_api.py

You can add a node to a network which already exists by using the following command

    python node_api.py -p 10003 -b 127.0.0.1 10002

This is however not really needed, as this will be done automatically in production.
"""
from __future__ import print_function
import requests
import json

NODE_ADDR = "http://127.0.0.1:9001"

SERVICE_NAME = "basic_service"

# Begin by registering your new service.
# This is done by POSTing to /register.
r = requests.post(NODE_ADDR + "/register", data=json.dumps({"service_name": SERVICE_NAME}))

if r.status_code == 200:
    # Now get the IP we just stored.
    r = requests.get(NODE_ADDR + "/" + SERVICE_NAME)
    print(json.loads(r.text))
else:
    print("Could not register this service! The node_api log may have some more details.")
