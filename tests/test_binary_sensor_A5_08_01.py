import unittest
from unittest import mock
from homeassistant.helpers.entity import Entity
from eltakobus.eep import Regular4BSMessage

from tests.test_binary_sensor_generic import TestBinarySensor

# mock update of Home Assistant
_entity_update_patch = mock.patch.object(Entity, "schedule_update_ha_state", return_value=None)

def setUpModule():
    _entity_update_patch.start()

def tearDownModule():
    _entity_update_patch.stop()
# EltakoBinarySensor.hass.bus.fire is mocked by class HassMock


class TestBinarySensor_A5_08_01(unittest.TestCase):
    """Test missing"""

    def test_occupancy_sensor(self):
        bs = TestBinarySensor().create_binary_sensor(eep_string="A5-08-01")

        self.assertEqual(bs._attr_is_on, None)

        msg = Regular4BSMessage (address=b'\xFF\xFF\x00\x80', data=b'\xaa\x80\x76\x0f', status=0x00)

        bs.value_changed(msg)
        self.assertEqual(bs._attr_is_on, True)

        msg.data = b'\xaa\x80\x76\x0d'
        bs.value_changed(msg)
        self.assertEqual(bs._attr_is_on, False)
