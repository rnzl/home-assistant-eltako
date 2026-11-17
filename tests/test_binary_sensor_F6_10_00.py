import unittest
from unittest import mock
from homeassistant.helpers.entity import Entity
from eltakobus.eep import F6_10_00, RPSMessage

from tests.test_binary_sensor_generic import TestBinarySensor

# mock update of Home Assistant
_entity_update_patch = mock.patch.object(Entity, "schedule_update_ha_state", return_value=None)

def setUpModule():
    _entity_update_patch.start()

def tearDownModule():
    _entity_update_patch.stop()
# EltakoBinarySensor.hass.bus.fire is mocked by class HassMock


class TestBinarySensor_F6_10_00(unittest.TestCase):

    def test_window_handle(self):
        bs = TestBinarySensor().create_binary_sensor(F6_10_00.eep_string)

        msg = RPSMessage(b'\xfe\xda\x65\x6d', 0x20, b'\xe0')
        bs.value_changed(msg)

        self.assertEqual(bs.is_on, True)

        msg = RPSMessage(b'\xfe\xda\x65\x6d', 0x20, b'\xf0')
        bs.value_changed(msg)

        self.assertEqual(bs.is_on, False)

    def test_window_handle_inverted_value(self):
        bs = TestBinarySensor().create_binary_sensor(F6_10_00.eep_string)
        bs.invert_signal = True

        msg = RPSMessage(b'\xfe\xda\x65\x6d', 0x20, b'\xe0')
        bs.value_changed(msg)

        self.assertEqual(bs.is_on, False)

        msg = RPSMessage(b'\xfe\xda\x65\x6d', 0x20, b'\xf0')
        bs.value_changed(msg)

        self.assertEqual(bs.is_on, True)
