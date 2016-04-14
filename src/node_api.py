#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from node import Node
from random import choice
from twisted.internet import reactor
from twisted.web.error import Error
from twisted.web.resource import NoResource
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.web.server import Site
from klein import run, route, Klein
import cgi
import json
import util

logger = util.create_logger("node_api.log")


class NodeAPI(Klein):
    app = Klein()

    def __init__(self, node):
        self.node = node

    @app.route("/register", methods=["POST"])
    def initiate_registration(self, request):
        """
        Determine whether there exists services of the same type, if so append
        the IP of this node to the list of IPs, otherwise create a new list of
        IPs.
        """
        json_data = json.loads(cgi.escape(request.content.read()))
        service_name = str(json_data["service_name"])

        deferred_result = self.node.get_value(service_name)
        deferred_result.addCallback(self.finish_registration,
                                    request, service_name)

        return NOT_DONE_YET

    def finish_registration(self, result, request, service_name):
        """
        Actually store the IP and service name of the current node, or return
        something that indicates that something went wrong.
        """
        node_ip = util.get_ip()
        service_ips = []

        if type(result) is dict:
            service_ips.extend(util.split_ips(result[service_name]))

        service_ips.append(node_ip)
        deferred_result = self.node.store_value(service_name,
                                            util.ips_to_string(service_ips))
        deferred_result.addCallback(self.async_return, request)
        logger.info("Registering {} as {}".format(node_ip, service_name))

        return NOT_DONE_YET

    @app.route("/<string:service_name>", methods=["GET"])
    def service(self, request, service_name):
        if service_name:
            deferred_result = self.node.get_value(service_name)
            deferred_result.addCallback(self.async_return, request)
            return NOT_DONE_YET

    def async_return(self, result, request):
        status_code = 200

        if result and not request.getHeader("Content-Type") == "application/json":
            ip = None
            for key, value in result.items():
                if type(value) is str:
                    result[key] = value.split(util.IP_DELIM)
                    ip = choice(result[key])

            request.write(json.dumps(ip))
        elif not result and request.getHeader("Content-Type") == "application/json":
            logger.info("Action successful!")
        else:
            status_code = 404

        request.setResponseCode(status_code)
        request.finish()

if __name__ == '__main__':

    args = util.parse_node_arguments()
    node = Node(logger, **vars(args))
    node_api = NodeAPI(node)

    node_api.app.run("localhost", 9001)
