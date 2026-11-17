"""Test setup for the standalone runtime.

IMPORTANT: these tests must run in their own pytest process:

    python -m tests.run_offline pytest eltako_standalone/tests

They activate the homeassistant shim via sys.path. If the real homeassistant
package was already imported (e.g. because the tests of the integration ran in
the same process), the suite fails rather than silently skipping it.
"""

import os
import sys
from unittest import mock

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from eltako_standalone.runtime import install_shim  # noqa: E402

install_shim()


def pytest_sessionfinish(session, exitstatus):
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    if exitstatus == pytest.ExitCode.OK and reporter and not reporter.stats.get("passed"):
        reporter.write_line("ERROR: standalone suite had no passing tests")
        session.exitstatus = pytest.ExitCode.TESTS_FAILED


@pytest.fixture(autouse=True)
def isolate_discovery(monkeypatch):
    """Standalone tests use fake discovery; never inspect the host's gateways."""
    from custom_components.eltako.tools import gateway_scan, plug_and_play

    async def no_mdns(_hass):
        return []

    monkeypatch.setattr(gateway_scan, "scan",
                        lambda _hass: {"ports": [], "gateways_without_port": []})
    monkeypatch.setattr(plug_and_play, "async_discover_mdns_gateways", no_mdns)
    monkeypatch.setattr(plug_and_play, "_bus_was_read", lambda *_args: True)


@pytest.fixture(autouse=True)
def disconnected_gateway_transport(monkeypatch):
    """Non-simulated fixture gateways have no physical transport."""
    from custom_components.eltako.core.gateway import EnOceanGateway

    def init_bus(gateway):
        gateway._received_message_count = 0
        gateway._bus = mock.Mock()
        gateway._bus.is_active.return_value = False
        gateway._bus.is_alive.return_value = False

    monkeypatch.setattr(EnOceanGateway, "_init_bus", init_bus)


CONFIG_YAML = """
eltako:
  general_settings:
    enable_frontend: True
    log_enocean_telegrams: True
  gateway:
  - id: 1
    device_type: fgw14usb
    base_id: FF-AA-80-00
    name: Test-Gateway
    auto_reconnect: False
    serial_path: /dev/tty.does-not-exist
    devices:
      light:
      - id: 00-00-00-01
        eep: M5-38-08
        name: Testlampe
        area: Kitchen
        sender: {id: 00-00-B0-01, eep: A5-38-08}
      binary_sensor:
      - id: ff-bb-0a-1b
        eep: F6-02-01
        name: Taster
"""


@pytest.fixture
def config_dir(tmp_path):
    (tmp_path / "configuration.yaml").write_text(CONFIG_YAML, encoding="utf-8")
    return str(tmp_path)


@pytest.fixture
def empty_config_dir(tmp_path):
    (tmp_path / "configuration.yaml").write_text(
        "eltako:\n  general_settings:\n    enable_frontend: True\n", encoding="utf-8")
    return str(tmp_path)
