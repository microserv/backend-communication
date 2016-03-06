# Service-to-service communication

### How to contribute
* Read the [contribution guidelines](https://github.com/microserv/contribution-guidelines)

### Development setup
1. Run ```setup.sh``` to install dependencies.
2. ???
3. Profit!

### Usage

Each node runs a web API on port 8080.
This API can be used to register/unregister services and get the IPs of an
abitary service.

The following guide describes how to use the API.

1. Begin by registering the service. This is done by POSTing to
   127.0.0.1:8080/register/<service_name>.
   Which will return a 200 status code if the registration was successful.
2. After doing this, you can obtain the IPs of a given service by sending a GET
   request to 127.0.0.1/<service_name>.
