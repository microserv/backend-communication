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
import cgi
import json
import util

logger = util.create_logger("node_api.log")


class NodeAPI(Resource):
    """
    Handles the basic routing of requests to the appropirate resource.
    '/{register, unregister}/<service_name>' maps to the 'Register' resource.
    '/<service_name>' maps to the 'Service' resource.
    """

    def __init__(self, node, web_port):
        Resource.__init__(self)
        self.node = node

        reactor.listenTCP(web_port, Site(self))
        logger.info("API listening on: {}".format(web_port))

    def getChild(self, request_str, request):
        request_str = request_str.strip()
        if request_str:
            if request_str and request_str in ['register', 'unregister']:
                return Register(self.node, request_str)
            else:
                return Service(self.node, request_str)
        else:
            return NoResource()


class Register(Resource):
    """
    Handles the registration and unregistration of a service.
    A service is registered in the DHT with the service name as the key,
    and a string of IPs to nodes of the service type as the value.
    """

    def __init__(self, node, register_action):
        Resource.__init__(self)
        self.node = node
        self.register_action = register_action

    def initiate_unregistration(self, request):
        json_data = json.loads(cgi.escape(request.content.read()))
        service_name = str(json_data["service_name"])

        deferred_result = self.node.get_value(service_name)
        deferred_result.addCallback(self.finish_unregistration,
                                    request, service_name)

        return NOT_DONE_YET

    def finish_unregistration(self, result, request, service_name):
        node_ip = util.get_ip()
        service_ips = []

        if type(result) is dict:
            service_ips.extend(util.split_ips(result[service_name]))

        try:
            service_ips.remove(node_ip)
            deferred_result = self.node.store_value(service_name,
                                                util.ips_to_string(service_ips))
            deferred_result.addCallback(self.async_success, request)
            logger.info("Unregistering {} as a {}".format(node_ip, service_name))

            return NOT_DONE_YET
        except ValueError:
            logger.info("{} is not registered".format(node_ip, service_name))
            request.setResponseCode(200)
            request.finish()


    def async_success(self, result, request):
        if not result or type(result) is list:
            logger.info("Action successful!")
            request.setResponseCode(200)
            request.finish()
        else:
            request.setResponseCode(500)
            request.finish()

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
        deferred_result.addCallback(self.async_success, request)
        logger.info("Registering {} as {}".format(node_ip, service_name))

        return NOT_DONE_YET

    def render_POST(self, request):
        if self.register_action == 'register':
            self.initiate_registration(request)
            return NOT_DONE_YET
        else:
            self.initiate_unregistration(request)
            return NOT_DONE_YET


class Service(Resource):

    def __init__(self, node, service_name):
        Resource.__init__(self)
        self.service_name = service_name
        self.node = node

    def async_success(self, result, request):
        if not result:
            request.setResponseCode(200)
            request.finish()
        else:
            request.setResponseCode(500)
            request.finish()

    def async_return(self, result, request):
        ip = None
        if result:
            if type(result) is dict:
                for key, value in result.items():
                    if type(value) is str:
                        result[key] = value.split(util.IP_DELIM)
                        ip = choice(result[key])

            request.write(json.dumps(ip))
            request.setResponseCode(200)
        else:
            request.setResponseCode(404)

        request.finish()

    def render_GET(self, request):
        deferred_result = self.node.get_value(self.service_name)
        deferred_result.addCallback(self.async_return, request)
        return NOT_DONE_YET

    def render_POST(self, request):
        json_data = json.loads(cgi.escape(request.content.read()))
        deferred_result = self.node.store_value(self.service_name,
                                               json_data["service_name"])
        deferred_result.addCallback(self.async_success, request)
        return NOT_DONE_YET


if __name__ == '__main__':

    args = util.parse_node_arguments()
    node = Node(logger, **vars(args))
    root = NodeAPI(node, 9001)

    reactor.run()
