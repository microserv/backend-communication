#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from entangled.node import EntangledNode
import netifaces as ni
import os
import sys
import twisted.internet.reactor
import util


class Node:

    def __init__(self, port, bootstrap):
        print('Creating Entangled Node on %s@%d...' % (self.get_ip("wlan0"), port))
        self.node = EntangledNode(udpPort=port)
        self.bootstrap_nodes = []

        if bootstrap:
            self.bootstrap_nodes.append(self.format_bootstrap_node_info(bootstrap))

        if self.bootstrap_nodes:
            print("Starting node with %d bootstrap nodes..." %  len(self.bootstrap_nodes))
            self.node.joinNetwork(self.bootstrap_nodes)
        else:
            self.node.joinNetwork()

    def format_bootstrap_node_info(self, node_info):
        return (node_info[0], int(node_info[1]))

    def handle_error(self, failure):
        print('An error has occurred:', failure.getErrorMessage())

    def get_value(self, key):
        print('Retrieving value from DHT for key "%s"...' % key)
        deferredResult = self.node.iterativeFindValue(key)
        deferredResult.addErrback(self.handle_error)
        return deferredResult

    def del_value(self, key):
        print('\nDeleting key/value from DHT...')
        deferredResult = node.iterativeDelete(key)
        deferredResult.addErrback(self.handle_error)

    def store_value(self, key, value):
        """ Stores the specified value in the DHT using the specified key """

        print('Soring value; Key: %s, Value: %s' % (key, value))
        deferredResult = self.node.iterativeStore(key, value)
        deferredResult.addErrback(self.handle_error)
        return deferredResult

    def get_ip(self, interface):
        ni.ifaddresses(interface)
        return ni.ifaddresses(interface)[2][0]['addr']

    def start(self):
        print("The network is now running.")
        twisted.internet.reactor.run()

    def stop(self):
        """ Stops the Twisted reactor, and thus the script """
        print('\nStopping Kademlia node and terminating script...')
        twisted.internet.reactor.stop()


if __name__ == '__main__':
    args = util.parse_node_arguments()

    node = Node(**vars(args))
    node.start()
