import unittest
from tests.mocks import GatewayMock
from unittest import mock
from homeassistant.helpers.entity import Entity
from homeassistant.const import Platform
from custom_components.eltako.binary_sensor import GatewayConnectionState

# mock update of Home Assistant
_entity_update_patch = mock.patch.object(Entity, "schedule_update_ha_state", return_value=None)

def setUpModule():
    _entity_update_patch.start()

def tearDownModule():
    _entity_update_patch.stop()
# EltakoBinarySensor.hass.bus.fire is mocked by class HassMock


class TestBinarySensor(unittest.TestCase):


    def test_GatewayConnectionState(self):
        gateway=GatewayMock()
        gateway._bus._is_active = False
        gateway.hass.create_task = lambda a: []
        bs = GatewayConnectionState(Platform.BINARY_SENSOR, gateway)

        bs.value_changed(True)
        self.assertEqual(bs._attr_is_on, True)

        bs.value_changed(False)
        self.assertEqual(bs._attr_is_on, False)

    def test_directly_online_GatewayConnectionState(self):
        gateway=GatewayMock()
        gateway._bus._is_active = True
        gateway.hass.create_task = lambda a: []
        bs = GatewayConnectionState(Platform.BINARY_SENSOR, gateway)

        bs.value_changed(True)
        self.assertEqual(bs._attr_is_on, True)

        bs.value_changed(False)
        self.assertEqual(bs._attr_is_on, False)

