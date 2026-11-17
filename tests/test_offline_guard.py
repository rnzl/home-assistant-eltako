"""The offline runner must reject physical devices and remote connections."""

import os
import socket
import tempfile
import unittest

from tests import offline_guard


@unittest.skipUnless(offline_guard.INSTALLED, "use the offline test runner")
class TestOfflineGuard(unittest.TestCase):
    def test_physical_serial_port_is_blocked(self):
        with self.assertRaises(PermissionError):
            open("/dev/ttyUSB0", "rb")

    def test_remote_connection_is_blocked(self):
        with socket.socket() as connection:
            with self.assertRaises(PermissionError):
                connection.connect(("192.0.2.1", 5100))

    def test_device_symlink_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "gateway")
            os.symlink("/dev/ttyUSB0", path)
            with self.assertRaises(PermissionError):
                open(path, "rb")

    def test_remote_datagram_is_blocked(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connection:
            with self.assertRaises(PermissionError):
                connection.sendto(b"test", ("192.0.2.1", 5100))
