# Service-to-service communication

[![Build Status](https://travis-ci.org/microserv/backend-communication.svg?branch=master)](https://travis-ci.org/microserv/backend-communication) [![Coverage Status](https://coveralls.io/repos/github/microserv/backend-communication/badge.svg?branch=master)](https://coveralls.io/github/microserv/backend-communication?branch=master)


### How to contribute
* Read the [contribution guidelines](https://github.com/microserv/contribution-guidelines)

### Development setup
1. Run ```setup.sh``` to install dependencies.
2. ???
3. Profit!

### Usage
`python node_api.py [-p [Internal port used by the nodes] -b [Known bootstrap IP] [Known bootstrap port]]`

Each node runs a HTTP API on port 9001.
This API can be used to register/unregister services and get the IP of an
abitary service.

### How to initilze the node and get an IP for another service.
1. Start the API using: `python node_api.py`
2. Register your service by POSTing to `http://127.0.0.1:9001/register` with the
   following payload: `{"service_name": "<YOUR SERVICE NAME HERE>"}`.
3. Obtain an IP to the service you want to connect to by submitting a GET
   request to `http:/127.0.0.1:9001/<service_name>`. This will return a single
   string containing the IP to an instance of the service.
