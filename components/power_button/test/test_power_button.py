from unittest.mock import Mock, call

import power_button_binding
from power_button_binding import KeyCodes

# POWER_BUTTON_PRESS_DEBOUNCE, from components/power_button/src/power_button.h.
PRESS_DEBOUNCE = 10


def test_press_event_is_sent_only_after_debounce() -> None:
    """
    .. test:: {{ pytest.test }}
       :id: TS_PB-005
       :tests: SWDD_PB-101, SWDD_PB-202, SWDD_PB-203
    """
    lib = power_button_binding.load()
    lib.powerButtonInit()
    lib.mocks.RteIsKeyPressed = Mock(return_value=True)
    lib.mocks.RteSetPowerKeyPressedEvent = Mock()

    for _ in range(PRESS_DEBOUNCE):
        lib.powerButton()

    lib.mocks.RteIsKeyPressed.assert_called_with(KeyCodes.POWER_BUTTON_KEY)
    assert lib.mocks.RteSetPowerKeyPressedEvent.call_args_list == [call(False)] * (PRESS_DEBOUNCE - 1) + [call(True)]
    assert lib.mocks.unexpected_calls == []
