"""Process-local guard for the offline test runners, not a security sandbox."""

import ipaddress
import os
import pty
import sys
from unittest import mock

INSTALLED = False


def install():
    """Block device opens and non-loopback sockets, except test-created PTYs."""
    global INSTALLED
    if INSTALLED:
        return
    pty_fds = []
    openpty = pty.openpty

    def tracked_openpty():
        master, slave = openpty()
        pty_fds.append(slave)
        return master, slave

    def test_pty(path):
        try:
            target = os.stat(path)
        except OSError:
            return False
        for fd in pty_fds:
            try:
                info = os.fstat(fd)
            except OSError:
                continue
            if (info.st_dev, info.st_ino) == (target.st_dev, target.st_ino):
                return True
        return False

    def local_address(address):
        if not isinstance(address, tuple):
            return True  # Unix-domain sockets
        host = address[0]
        if host == "localhost":
            return True
        try:
            return ipaddress.ip_address(host).is_loopback
        except ValueError:
            return False

    def audit(event, args):
        if event == "open" and isinstance(args[0], (str, bytes, os.PathLike)):
            path = os.path.realpath(os.fsdecode(args[0]))
            if (path == "/dev" or path.startswith("/dev/")) and path not in {
                "/dev/null", "/dev/zero", "/dev/random", "/dev/urandom", "/dev/pts/ptmx",
            } and not test_pty(path):
                raise PermissionError(f"offline tests blocked device access: {path}")
        if event in {"socket.connect", "socket.bind", "socket.sendto"}:
            if not local_address(args[1]):
                raise PermissionError(f"offline tests blocked network access: {args[1]}")
        if event == "socket.getaddrinfo" and args[0] is not None:
            if not local_address((args[0], 0)):
                raise PermissionError(f"offline tests blocked DNS lookup: {args[0]}")

    pty.openpty = tracked_openpty
    sys.addaudithook(audit)
    INSTALLED = True


def isolate_port_discovery():
    """Use empty host discovery while retaining tests' explicit fake port fixtures."""
    from serial.tools import list_ports
    from custom_components.eltako.tools import gateway_scan

    read_sysfs = gateway_scan._read_sysfs_info

    def read_test_sysfs(device, sysfs_tty_dir=gateway_scan.SYSFS_TTY_DIR):
        if sysfs_tty_dir == gateway_scan.SYSFS_TTY_DIR:
            return {}
        return read_sysfs(device, sysfs_tty_dir=sysfs_tty_dir)

    patches = [
        mock.patch.object(list_ports, "comports", return_value=[]),
        mock.patch.object(gateway_scan, "DEVICE_GLOBS", []),
        mock.patch.object(gateway_scan, "SERIAL_BY_ID_DIR", ""),
        mock.patch.object(gateway_scan, "SERIAL_BY_PATH_DIR", ""),
        mock.patch.object(gateway_scan, "_read_sysfs_info", read_test_sysfs),
    ]
    for patch in patches:
        patch.start()
    return patches
