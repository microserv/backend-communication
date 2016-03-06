#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from node import Node
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.web.server import Site
import argparse
import cgi
import json
import util


class NodeAPI(Resource):

    def __init__(self, node):
        Resource.__init__(self)
        self.node = node

    def getChild(self, request_str, request):
        if request_str in ['register', 'unregister']:
            return Register(self.node, request_str)
        else:
            return Service(self.node, request_str)

class Register(Resource):

    def __init__(self, node, register_action):
        Resource.__init__(self)
        self.node = node
        self.register_action = register_action

    def unregister(self, service_name):
        pass

    def async_success(self, result, request):
        if not result:
            print("Action successful!")
            request.setResponseCode(200)
            request.finish()
        else:
            request.setResponseCode(500)
            request.finish()

    def initiate_registration(self, request):
        json_data = json.loads(cgi.escape(request.content.read()))
        service_name = str(json_data["value"])

        deferred_result = self.node.get_value(service_name)
        deferred_result.addCallback(self.finish_registration, request, service_name)
        return NOT_DONE_YET

    def finish_registration(self, result, request, service_name):
        node_ip = self.node.get_ip("wlan0")
        service_ips = []

        if type(result) is dict:
            service_ips.extend(util.split_ips(result[service_name]))

        service_ips.append(node_ip)
        deferred_result = self.node.store_value(service_name,
                                               util.ips_to_string(service_ips))
        deferred_result.addCallback(self.async_success, request)
        print("Registering {} as {}".format(node_ip, service_name))

        return NOT_DONE_YET

    def render_POST(self, request):
        if self.register_action == 'register':
            self.initiate_registration(request)
            return NOT_DONE_YET
        else:
            self.unregister(service_name)
            return 404

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
        request.write(json.dumps(result))
        request.finish()

    def render_GET(self, request):
        deferredResult = self.node.get_value(self.service_name)
        deferredResult.addCallback(self.async_return, request)
        return NOT_DONE_YET

    def render_POST(self, request):
        json_data = json.loads(cgi.escape(request.content.read()))
        deferredResult = self.node.store_value(self.service_name,
                                               json_data["value"])
        deferredResult.addCallback(self.async_success, request)
        return NOT_DONE_YET


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, help="Usage: PORT_TO_USE")
    parser.add_argument("-f", "--boostrap_file",
                        help="Usage: -f FILENAME_TO_FILE_WITH_KNOWN_NODES")
    parser.add_argument("-b", "--bootstrap", nargs=2,
                        help="Usage: KNOWN_NODE_IP KNOWN_NODE_PORT")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    node = Node(**vars(args))
    root = NodeAPI(node)
    site = Site(root)

    reactor.listenTCP(args.port + 1, site)
    print("API listening on:", args.port+1)
    reactor.run()
