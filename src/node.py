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

    def __init__(self, logger, port, bootstrap_node=None):
        self.logger = logger
        self.logger.info('Creating Entangled Node on %s:%d...' % (self.get_ip("wlan0"), port))
        self.node = EntangledNode(udpPort=port)

        if bootstrap_node:
            self.logger.info("Connecting to network through: %s:%s" % (bootstrap_node[0], bootstrap_node[1]))
            formatted_bootstrap_node = self.format_bootstrap_node_info(bootstrap_node)
            self.node.joinNetwork([formatted_bootstrap_node])
        else:
            self.node.joinNetwork()

        logger.info('Node created!')

    def format_bootstrap_node_info(self, node_info):
        return (node_info[0], int(node_info[1]))

    def handle_error(self, failure):
        self.logger.error('An error has occurred:', failure.getErrorMessage())

    def get_value(self, key):
        self.logger.info('Retrieving "%s"...' % key)
        deferred_result = self.node.iterativeFindValue(key)
        deferred_result.addErrback(self.handle_error)
        return deferred_result

    def del_value(self, key):
        self.logger.info('\nDeleting: "%s"' % key)
        deferred_result = node.iterativeDelete(key)
        deferred_result.addErrback(self.handle_error)

    def store_value(self, key, value):
        """ Stores the specified value in the DHT using the specified key """

        self.logger.info('Soring "%s" -> "%s"' % (key, value))
        deferred_result = self.node.iterativeStore(key, value)
        deferred_result.addErrback(self.handle_error)
        return deferred_result

    def get_ip(self, interface):
        ni.ifaddresses(interface)
        return ni.ifaddresses(interface)[2][0]['addr']
