"""Fan platform used by the standalone runtime."""

from enum import IntFlag

from ...helpers.entity import Entity


class FanEntityFeature(IntFlag):
    SET_SPEED = 1
    OSCILLATE = 2
    DIRECTION = 4
    PRESET_MODE = 8
    TURN_OFF = 16
    TURN_ON = 32


class FanEntity(Entity):
    @property
    def percentage(self):
        return getattr(self, "_attr_percentage", 0)

    @property
    def is_on(self):
        return self.percentage is not None and self.percentage > 0

    @property
    def state(self):
        return "on" if self.is_on else "off"

    @property
    def capability_attributes(self):
        if self.supported_features & FanEntityFeature.SET_SPEED:
            return {"preset_modes": None}
        return None

    @property
    def state_attributes(self):
        if self.supported_features & FanEntityFeature.SET_SPEED:
            return {"percentage": self.percentage, "percentage_step": 1.0,
                    "preset_mode": None}
        return None
