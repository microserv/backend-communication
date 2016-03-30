import unittest
from node import Node
from twisted.internet import reactor
from threading import Thread

class TestNodeSetup(unittest.TestCase):

    def setUp(self):
        self.node = Node(None, 12345, ('127.0.0.1', 12346))

    def test_setup(self):
        self.assertEqual(self.node._listeningPort.port, 12345, "Port set incorrectly!")

    def tearDown(self):
        self.node = None

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNodeSetup)
    test_runner = unittest.TextTestRunner()
    test_runner.run(suite)
