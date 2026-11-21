---
status: Ready
priority: Medium
blocked_by: [YANGA-010]
---

# [SPLED-005] MVP of pytest tests for a component and a variant

## Summary

As the maintainer of yanga, I want SPLedY to use the new `pytest` testing block for one component and one variant, so that the pytest test framework is tried on a real product line before it is released.

## Description

yanga gets a `pytest` testing block (YANGA-010): the component or variant is built as a shared library, the missing functions are forwarded to Python, and the block's pytest files drive it through a generated binding. SPLedY already drives the Disco variant from pytest by hand on the `pc_gui` platform. This item tries the new block locally, with editable installs of yanga and clanguru, before either is released.

## Scope decisions

- **A new `pytest` platform** that lists the pytest generator and the report generators, with the gtest platform's host toolchain. The gtest platform and the hand-written `pc_gui` integration tests stay as they are.
- **`light_controller`:** the test mocks `RteGetPowerState` and the other `RteGet...` calls in Python, calls `lightController()`, and checks the colour passed to `RteSetLightValue`, a struct (`RGBColor`) that the mock reads through a pointer.
- **Disco:** the test calls `Task_Init()` and then `spled()` step by step, plays the platform in Python (`ButtonInterfaceIsButtonPressed`, the LED and button interface functions), and reads the light the variant computed.
- **Local first.** The item is worked on locally with editable installs of clanguru and yanga; nothing is pushed until they are released.
- **Out of scope:** moving other tests to pytest, and the yanga and clanguru floor bumps (they follow the release).

## Acceptance criteria

- [ ] On the `pytest` platform, `light_controller` has a `pytest` block whose test mocks `RteGetPowerState` in Python and checks the `RGBColor` passed to `RteSetLightValue`, and the component report shows its result and coverage
- [ ] On the `pytest` platform, Disco has a `pytest` block whose test presses the power button through a Python mock of `ButtonInterfaceIsButtonPressed` and sees the light turn on, and the variant report shows its result
- [ ] The existing gtest and integration tests pass as before
