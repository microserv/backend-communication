import unittest
from node import Node
from twisted.internet import reactor
from threading import Thread

class NodeSetup(unittest.TestCase):
    def setUp(self):
        self.node = Node(12345, ('127.0.0.1', 12346), None)

    def test_setup(self):
        self.assertEqual(self.node.node._listeningPort.port, 12345, "Port set incorrectly!")
        self.assertEqual(self.node.bootstrap_nodes, [('127.0.0.1', 12346)], "Bootstrap not not set correctly!")

    def tearDown(self):
        self.node = None

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(NodeSetup)
    test_runner = unittest.TextTestRunner()
    test_runner.run(suite)


