# Service-to-service communication

### How to contribute
* Read the [contribution guidelines](https://github.com/microserv/contribution-guidelines)

### Development setup
1. Run ```setup.sh``` to install dependencies.
2. ???
3. Profit!

### Usage

Each node runs a HTTP API on port 9001.
This API can be used to register/unregister services and get the IPs of an
abitary service.

### How to use this API with a service
Let's assume you want to use the microauth service. This can by done by:

1. Obtain the IP of the service. This is done by making a GET request to the
   local node. This node should always run on port 9001.
   You can obtain the IP to an instance of the microauth service by issuing the
   following request: `curl http://127.0.0.1:9001/microauth` this will return
   a JSON array with the IPs too all the instances.
