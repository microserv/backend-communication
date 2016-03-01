# -*- coding: utf-8 -*-
from flask import Flask, abort, jsonify, request
from flask_restful import Resource, Api
from node import Node
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
import argparse

app = Flask(__name__)
api = Api(app)
SUCCESS = 200


class NodeAPI(Resource):
    def __init__(self, node):
        self.node = node

    def get(self, service_name=None):
        if service_name:
            self.node.get_value(service_name)
            return SUCCESS

    def post(self, service_name=None):
        if not request.json or "value" not in request.json or not service_name:
            abort(400)
        else:
            self.node.store_value(service_name, request.json["value"])
            return SUCCESS


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, help="Usage: PORT_TO_USE")
    parser.add_argument("-f", "--boostrap_file",
                        help="Usage: -f FILENAME_TO_FILE_WITH_KNOWN_NODES")
    parser.add_argument("-b", "--bootstrap", nargs=2,
                        help="Usage: KNOWN_NODE_IP KNOWN_NODE_PORT")
    return parser.parse_args()


def init_api(api):
    api.add_resource(NodeAPI, "/<string:service_name>",
                     resource_class_kwargs={'node': node})
    resource = WSGIResource(reactor, reactor.getThreadPool(), app)
    return Site(resource)


if __name__ == '__main__':
    args = parse_arguments()
    node = Node(**vars(args))
    site = init_api(api)

    reactor.listenTCP(8080, site)
    reactor.run()
