from unittest import mock
from homeassistant.helpers.entity import Entity

from tests.test_binary_sensor_F6_02_01 import TestBinarySensor_F6_02_01

# mock update of Home Assistant
_entity_update_patch = mock.patch.object(Entity, "schedule_update_ha_state", return_value=None)

def setUpModule():
    _entity_update_patch.start()

def tearDownModule():
    _entity_update_patch.stop()
# EltakoBinarySensor.hass.bus.fire is mocked by class HassMock


class TestBinarySensor_F6_02_02(TestBinarySensor_F6_02_01):
    """Same as F6-02-01"""
