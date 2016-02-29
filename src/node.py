#!/usr/bin/env python

import os, sys, time, signal, argparse
import twisted.internet.reactor
from entangled.node import EntangledNode
from entangled.kademlia.datastore import SQLiteDataStore
import netifaces as ni

class Node:

    def __init__(self, port, bootstrap, boostrap_file):
        self.init_datastore('/tmp/dbFile%s.db' % port)
        print 'Creating Entangled Node on %s@%d...' % (self.get_ip("wlan0"), port)
        self.node = EntangledNode(udpPort=port, dataStore=self.data_store)
        self.start()

    def init_datastore(self, filename):
        if os.path.isfile(filename):
            os.remove(filename)

        self.data_store = SQLiteDataStore(dbFile = filename)


    def handle_error(self, failure):
        print 'An error has occurred:', failure.getErrorMessage()


    def get_value(self, key):
        print 'Retrieving value from DHT for key "%s"...' % key
        deferredResult = self.node.iterativeFindValue(key)
        deferredResult.addErrback(handle_error)

    def del_val(self, key):
        print '\nDeleting key/value from DHT...'
        deferredResult = node.iterativeDelete(key)
        deferredResult.addErrback(handle_error)


    def store_val(self, key, value):
        """ Stores the specified value in the DHT using the specified key """

        print 'Soring value; Key: %s, Value: %s' % (key, value)
        deferredResult = self.node.iterativeStore(key, value)
        deferredResult.addErrback(self.handle_error)


    def get_ip(self, interface):
        ni.ifaddresses(interface)
        return ni.ifaddresses(interface)[2][0]['addr']


    def start(self):
        print 'Starting network...'
        self.node.joinNetwork()
        print "The network is now running."
        twisted.internet.reactor.run()


    def stop(self):
        """ Stops the Twisted reactor, and thus the script """
        print '\nStopping Kademlia node and terminating script...'
        twisted.internet.reactor.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, help="Usage: PORT_TO_USE")
    parser.add_argument("-f", "--boostrap_file", help="Usage: -f FILENAME_TO_FILE_WITH_KNOWN_NODES")
    parser.add_argument("-b", "--bootstrap", nargs=2, help="Usage: KNOWN_NODE_IP KNOWN_NODE_PORT")
    args = parser.parse_args()

    node = Node(**vars(args))
