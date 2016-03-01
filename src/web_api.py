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

class NodeAPI(Resource):
    def __init__(self, node):
        Resource.__init__(self)
        self.node = node

    def getChild(self, service_name, request):
        return Service(self.node, service_name)

    def post(self, service_name=None):
        if not request.json or "value" not in request.json or not service_name:
            abort(400)
        else:
            successful = self.node.store_value(str(service_name), str(request.json["value"]))

            if successful:
                return SUCCESS
            else:
                return abort(500)

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
        deferredResult = self.node.store_value(self.service_name, json_data["value"])
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
    print "API listening on:", args.port+1
    reactor.run()
