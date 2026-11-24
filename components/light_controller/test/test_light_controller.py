import json
from pathlib import Path
from unittest.mock import Mock

import pytest

import light_controller_binding
from light_controller_binding import PowerState

# The tests and their specs exist only in a blinking variant, as the gtest tests under `#if CONFIG_BLINKING`:
# Sleep and Spa build this scope too, without blinking, purple and with brightness adjustment, and their
# reports have no SWDD_LC-101 to link. The expected values are Disco's: green at the fixed brightness of 128.
# KConfigGen writes the variant's feature selection to <build>/kconfig/autoconf.json; the binding is in <build>/light_controller.
FEATURES = json.loads((Path(light_controller_binding.__file__).parents[1] / "kconfig" / "autoconf.json").read_text())
if FEATURES["BLINKING"]:
    @pytest.mark.parametrize(("main_knob_value", "blink_period"), [(30, 70), (95, 10)])
    def test_blink_period_follows_the_main_knob_down_to_a_minimum(main_knob_value: int, blink_period: int) -> None:
        """
        .. test:: {{ pytest.test }}
           :id: TS_LC-007
           :tests: SWDD_LC-101
        """
        lib = light_controller_binding.load()

        assert lib.calculateBlinkPeriod(main_knob_value) == blink_period

    def test_power_on_turns_the_light_green() -> None:
        """
        .. test:: {{ pytest.test }}
           :id: TS_LC-008
           :tests: SWDD_LC-100, SWDD_LC-103, SWDD_LC-201, SWDD_LC-202
        """
        lib = light_controller_binding.load()
        lib.mocks.RteGetPowerState = Mock(return_value=PowerState.POWER_STATE_ON)
        lib.mocks.RteGetMainKnobValue = Mock(return_value=50)
        light_values = []
        lib.mocks.RteSetLightValue = Mock(side_effect=lambda color: light_values.append((color.red, color.green, color.blue)))

        lib.lightController()

        # CONFIG_COLOR_GREEN at the default brightness of 128.
        assert light_values == [(0, 128, 0)]
        assert lib.mocks.unexpected_calls == []
