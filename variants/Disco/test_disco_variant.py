import ctypes
from unittest.mock import Mock

import Disco_binding
from Disco_binding import KeyCodes, PowerState, RGBColor


def test_holding_the_power_button_turns_the_light_green() -> None:
    lib = Disco_binding.load()
    lib.mocks.ButtonInterfaceIsButtonPressed = Mock(return_value=True)
    lib.mocks.ledInterface = Mock()

    for _ in range(10):
        lib.spled()

    assert lib.RteGetPowerState() == PowerState.POWER_STATE_ON
    assert lib.mocks.ledInterface.call_count == 10
    light_value = RGBColor()
    lib.RteGetLightValue(ctypes.byref(light_value))
    assert light_value.green == 128
    assert lib.mocks.unexpected_calls == []


def test_blinking_flashes_at_most_three_times_per_second() -> None:
    lib = Disco_binding.load()
    lib.mocks.ButtonInterfaceIsButtonPressed = Mock(side_effect=lambda key: key == KeyCodes.POWER_BUTTON_KEY)
    lib.mocks.ledInterface = Mock()
    lib.RteSetMainKnobValue(100)
    for _ in range(20):
        lib.spled()
    assert lib.RteGetPowerState() == PowerState.POWER_STATE_ON

    # One second of 10 ms task cycles: a flash is the light going on and off, so three flashes are six changes.
    light_values = []
    for _ in range(100):
        lib.spled()
        light_value = RGBColor()
        lib.RteGetLightValue(ctypes.byref(light_value))
        light_values.append((light_value.red, light_value.green, light_value.blue))
    changes = sum(before != after for before, after in zip(light_values, light_values[1:]))

    assert 0 < changes <= 6
    assert lib.mocks.unexpected_calls == []
