import ctypes
from unittest.mock import Mock

import test_integrations_spled_binding
from test_integrations_spled_binding import PowerState, RGBColor


def test_holding_the_power_button_turns_the_light_green() -> None:
    """
    .. test:: {{ pytest.test }}
       :id: TS_SPLED-001
       :tests: SWDD_PB-101, SWDD_PSP-001, SWDD_PSP-002, SWDD_LC-100, SWDD_LC-103
    """
    lib = test_integrations_spled_binding.load()
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
