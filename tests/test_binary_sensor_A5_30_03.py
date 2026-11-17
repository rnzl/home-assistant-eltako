import unittest
from unittest import mock
from homeassistant.helpers.entity import Entity, EntityDescription
from eltakobus.eep import A5_30_03, Regular4BSMessage

from tests.test_binary_sensor_generic import TestBinarySensor

# mock update of Home Assistant
_entity_update_patch = mock.patch.object(Entity, "schedule_update_ha_state", return_value=None)

def setUpModule():
    _entity_update_patch.start()

def tearDownModule():
    _entity_update_patch.stop()
# EltakoBinarySensor.hass.bus.fire is mocked by class HassMock


class TestBinarySensor_A5_30_03(unittest.TestCase):

    def test_digital_input(self):

        for key in ["0", "1", "2", "3", "wake"]:
            bs = TestBinarySensor().create_binary_sensor(A5_30_03.eep_string, description= EntityDescription(key=key, name=key))

            msg = Regular4BSMessage(b'\00\x00\x00\x01', 0x20, b'\00\x00\x1F\x08')
            bs.value_changed(msg)

            self.assertEqual(bs.is_on, True)

            msg = Regular4BSMessage(b'\00\x00\x00\x01', 0x20, b'\00\x00\x00\x08')
            bs.value_changed(msg)

            self.assertEqual(bs.is_on, False)


    def test_inverted_digital_input(self):

        for key in ["0", "1", "2", "3", "wake"]:
            bs = TestBinarySensor().create_binary_sensor(A5_30_03.eep_string, description= EntityDescription(key=key, name=key))
            bs.invert_signal = True

            msg = Regular4BSMessage(b'\00\x00\x00\x01', 0x20, b'\00\x00\x1F\x08')
            bs.value_changed(msg)

            self.assertEqual(bs.is_on, False)

            msg = Regular4BSMessage(b'\00\x00\x00\x01', 0x20, b'\00\x00\x00\x08')
            bs.value_changed(msg)

            self.assertEqual(bs.is_on, True)
