#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from entangled.node import EntangledNode
import netifaces as ni


class Node(EntangledNode):
    """
    The 'Node' is a wrapper around the EntangledNode class.
    This wrapper provides several functions for adding, deleting, and receiving
    key/value pairs from the DHT network.
    """

    def __init__(self, logger, port, bootstrap_node=None):
        super(EntangledNode, self).__init__(udpPort=port)

        self.logger = logger
        self.logger.info('Creating Entangled Node on %s:%d...' % (self.get_ip("wlan0"), port))

        # A bootstrap node consists of an IP and port to a known node in the
        # network we want to join.
        if bootstrap_node:
            self.logger.info("Connecting to network through: %s:%s" % (bootstrap_node[0], bootstrap_node[1]))

            formatted_bootstrap_node = self._format_bootstrap_node_info(bootstrap_node)
            self.joinNetwork([formatted_bootstrap_node])
        else:
            self.joinNetwork()

        logger.info('Node created!')

    def _format_bootstrap_node_info(self, node_info):
        """
        Format lists of the format [IP, Port] into tuples readable by an
        Entangled node.
        """
        return (node_info[0], int(node_info[1]))

    def handle_error(self, failure):
        self.logger.error('An error has occurred:', failure.getErrorMessage())

    def get_value(self, key):
        """
        Attempt to obtain a value from the DHT.
        The key 'key' is a string of arbitrary length.
        """
        self.logger.info('Retrieving "%s"...' % key)

        # Query the other nodes in the network to determine whether they have
        # this key.
        deferred_result = self.iterativeFindValue(key)
        deferred_result.addErrback(self.handle_error)

        return deferred_result

    def del_value(self, key):
        """
        Attempt to delete a value from the DHT.
        """
        self.logger.info('\nDeleting: "%s"' % key)
        # Query the other nodes in the network to find and delete the key/value
        # pair.
        deferred_result = self.iterativeDelete(key)
        deferred_result.addErrback(self.handle_error)

        return deferred_result

    def store_value(self, key, value):
        """
        Stores the specified value in the DHT using the specified key.
        The key 'key' and value 'value' must both be strings.
        """
        self.logger.info('Soring "%s" -> "%s"' % (key, value))
        # Attempt to find the closest neighbour node and store the value there.
        # If no nodes are close enough, store it in this node.
        deferred_result = self.iterativeStore(key, value)
        deferred_result.addErrback(self.handle_error)

        return deferred_result

    def get_ip(self, interface):
        """
        Get the IPv4 address of the interface with name 'interface'.
        Returns the IPv4 address as a string.
        """
        return ni.ifaddresses(interface)[2][0]['addr']
