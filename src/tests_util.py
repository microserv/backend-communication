import unittest
import util

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.ips_as_string = "192.168.0.1" + util.IP_DELIM + "192.168.0.2"
        self.ips = ["192.168.0.1", "192.168.0.2"]

    def test_ip_formatting(self):
        self.assertEqual(self.ips_as_string, util.ips_to_string(self.ips), "Could not format IPs correctly!")
        self.assertEqual(self.ips, util.split_ips(self.ips_as_string), "Could not format IPs correctly!")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    test_runner = unittest.TextTestRunner()
    test_runner.run(suite)


