---
status: Done (2026-11-24)
priority: Medium
blocked_by: [YANGA-013, YANGA-014]
---

# [SPLED-008] pytest tests for components, an integration component and the Disco variant

## Summary

As the maintainer of yanga, I want SPLedY to test components, an integration component and the Disco variant with the new `pytest` testing block, so that the pytest test framework is tried on a real product line before yanga is released.

## Description

SPLedY tests with gtest only, plus a hand-made pytest test of the Disco variant through the `pc_gui` shared library. yanga's pytest test framework (YANGA-013) builds a test library per test scope, generates a binding and Python mocks with clanguru (CLG-019), and reports results and coverage per framework (YANGA-012). SPLedY is its first user.

## What exists

- [AGENTS.md](../../AGENTS.md), [doc/software_architecture/index.md](../../doc/software_architecture/index.md), [doc/platforms/pc_gui.md](../../doc/platforms/pc_gui.md).
- [components/yanga.yaml](../../components/yanga.yaml): the `testing:` blocks, `light_controller`, the integration component `test_integrations_spled`.
- [variants/Disco/yanga.yaml](../../variants/Disco/yanga.yaml): the variant's gtest block.
- [platforms/test/yanga.yaml](../../platforms/test/yanga.yaml): the generators of the `test` platform (named `gtest` before this item).
- [platforms/pc_gui/spled_lib.py](../../platforms/pc_gui/spled_lib.py), [test/test_Disco.py](../../test/test_Disco.py): the hand-written binding and test.
- [doc/components.md](../../doc/components.md), [doc/containers.md](../../doc/containers.md): the report pages by kind.

## Scope decisions

- **Three test scopes: component, integration component and variant.** The framework is for any of them, and SPLedY starts with one or two tests per scope. An integration component (one with `integrates:`) already compiles the sources of the components it integrates, so yanga-core does not change.
- **Missing functions are mocked in Python.** For every function a test scope calls but does not define, a generated C function (a trampoline) forwards the call to a Python callable the test sets, for example a `unittest.mock.Mock`. Hand-written C fakes in `mockup_sources` stay possible for any function a trampoline cannot forward. Rejected: gmock mocks with their default action, because Python cannot set them; generated C stubs with counters and return values, because every hard case (a value per call, out-parameters, callbacks) would need its own C design, which `unittest.mock` already gives in Python.
- **A call with no Python mock set** returns a zero-initialised value of the return type and is recorded; the binding offers the list as `lib.mocks.unexpected_calls`. A test checks it if it wants. Rejected: failing the test automatically, because that needs a pytest plugin.
- **The variant scope** links the same components as the gtest variant test (no containers, no integration components), in the variant's `variant_test` folder; its files are named `<variant>_pytest` and `<variant>_binding`, and it writes its gcov data to its own `GCOV_PREFIX` folder.
- **File names in the test scope's build folder.** For the test scope `light_controller`, yanga calls `clanguru bind --filename light_controller_binding --library-name light_controller_pytest`. The folder holds `light_controller_pytest.dylib` (`.so`, `.dll`), `light_controller_binding.py`, `light_controller_binding_mocks.c` and `light_controller_pytest_junit.xml`. The `_binding` suffix keeps the module name apart from any test file or component name.
- **pytest runs in the interpreter that runs yanga.** pytest is a dependency of the project, not of yanga. yanga checks for pytest when it generates the build files and stops with a message that names pytest; it writes `<python> -m pytest` with the interpreter it runs in. pytest runs in the project folder, with the test files given by path and `-p no:cacheprovider`.
- **The pytest block's mocking config has gtest's shape and merge rule.** `config.mocking.strict` and `config.mocking.exclude_symbol_patterns`, on the block and on the platform's generator config, the block's values over the platform's; they are passed to `clanguru bind`. It reuses yanga-core's `MockingConfig`; `enabled: false` is an error that names the field, because pytest always needs the mocks. Rejected: one mocking entry shared with gtest, because pytest would then read gtest's settings and break on a platform without the gtest generator.
- **Generator order.** A platform lists the pytest generator after the gtest generator and before `TestResultsCMakeGenerator`, `SphinxTestReportCMakeGenerator` and `ReportCMakeGenerator`, which read what it registers.
- **A collector generator, `TestResultsCMakeGenerator` (module `yanga.cmake.test_results`).** A platform lists it after its test generators. It creates the phony `<name>_test`, `<name>_coverage` and `<name>_report` targets, merges the coverage tracefiles per entry, and writes the Coverage pages and the merged coverage pages. The test generators only build, run and register. Rejected: gtest collecting for every framework, because pytest would then define the same targets again, gtest merges before a generator listed after it has registered anything, and pytest must work without gtest; `SphinxTestReportCMakeGenerator` collecting, because its job is the results report and a platform without it would lose its coverage; gtest collecting only when no collector is listed, because that is two code paths for one job. This breaks platforms that test: they must list the new generator. Accepted, because yanga-core is at 0.x and yanga is in alpha.
- **Order and release.** clanguru `bind` first, released. YANGA-012 in parallel, as it does not need clanguru. Then the yanga pytest generator, blocked by both. Then SPLedY, with editable installs of clanguru and yanga, before the yanga release; yanga is released only when SPLedY is green.
- **The items of the earlier planning run are removed.** CLG-017 and SPLED-005 are deleted by a `docs(backlog)` commit each, since their origin commits have work on top; YANGA-010 and a duplicate local clanguru commit were dropped when the local `main` branches were reset to origin. New items get new IDs.
- **SPLED-005 is set Superseded, not deleted (2026-11-24).** The human's rule: "once an item was pushed and the comit can not be amended, then it shall not just dissapear otherwise it will look like some indexes were skipped". SPLED-005 was added in `2fa3a7e`, which has work on top on `develop`, so it stays in `docs/backlog/` as Superseded, with `related: [SPLED-008]`. This replaces the removal in the decision above, in plan step 6 and in the third acceptance criterion.
- **SPLedY's `gtest` platform is renamed `test` (2026-11-24, the human's decision after the first run: "keep one platform, rename it to test").** It runs gtest and pytest in one build, so one report shows both frameworks and one coverage that merges them; a platform named after one framework misleads. One platform stays; rejected: a separate `pytest` platform, because its report would not merge the coverage. A platform may still list only one test generator with `TestResultsCMakeGenerator`. Report paths change from `.yanga/build/variants/<variant>/gtest/` to `.yanga/build/variants/<variant>/test/`. The nine platform-named tests in `test/test_Disco.py` are renamed from `test_gtest_*` to `test_platform_*` (the fixture `gtest_build_dir` to `test_platform_build_dir`), none deleted; the floor guard lists the old names as deleted tests, and this rename is the wanted change.
- **pytest traceability is part of SB-009 (2026-11-24, approved by the human).** The plan the human approved: "SPLED-008 grows: blocked by the new item; its pytest tests get test specs with `tests:` links, and `conf.py` gets the `results` rule for pytest's names, so `test-results-required` covers them". The new item is YANGA-014.

## What users see

- **The `test` platform (renamed from `gtest`) lists the pytest generator and `TestResultsCMakeGenerator`, and SPLedY has pytest tests for one or two components, one integration component and the Disco variant.** Not breaking: the gtest tests stay. UAT: yes, the reports show both frameworks. Why: the first real use of the framework before yanga is released. Approved by the human (2026-11-24)

## Out of scope

Removing the `pc_gui` platform or its hand-written test.

## Acceptance criteria

- [x] UAT: in the report of the `test` platform, `light_controller`, `power_button`, one integration component and the Disco variant each show a "Test results" page with a gtest and a pytest section, and a "Coverage" page with one gcovr section that counts both: a line only a pytest test reaches is shown as covered. Check: `yanga run --variant Disco --platform test --target report`, then the human reads the report.
- [x] The existing tests still pass. Check: `pytest test`.
- [x] SPLED-005 of the earlier planning run is Superseded by SPLED-008. Check: `jarvis backlog show`.
- [x] UAT: every pytest test of `light_controller`, `power_button` and the integration component has a test spec that links to the specs it tests and to its pytest result, and `test-results-required` covers them (the variant's test sources are not rendered, for pytest as for gtest). Check: the report build passes, then the human reads the report.

## Plan

1. `platforms/test/yanga.yaml`: list `PytestCMakeGenerator` after the gtest generator, then `TestResultsCMakeGenerator`, before the report generators, with `mocking.strict: false` and `mocking.exclude_symbol_patterns: ["_*"]`, as for gtest.
2. `components/yanga.yaml`, component `test/` folders: a `pytest` block and one or two tests each for `light_controller` and `power_button`, with the `Rte...` calls mocked in Python.
3. `components/yanga.yaml`: a `pytest` block and a test for `test_integrations_spled`.
4. `variants/Disco`: a `pytest` block and a test `variants/Disco/test_disco_variant.py` (the module name `test_disco` would clash with `test/test_Disco.py`) that steps the variant with the button and LED interfaces mocked in Python.
5. Install the local clanguru and yanga with `.venv/bin/pip install -e` after every bootstrap, because the install steps reinstall from the lock; build the report; the human does the UAT.
6. `docs/backlog`: remove `spled-005.md`.

## Questions

- **Where is the variant's pytest coverage fixed?** `yanga run --variant Disco --platform gtest --target report` fails with exit 64 in `variant_test/Disco_pytest_gcovr.cfg`: gcov finds `Disco_binding_mocks.c.gcda` under the variant's `GCOV_PREFIX` with no `.gcno`. SPLedY's `platforms/gtest/gcc.cmake` adds `-fcondition-coverage` to every C object, so the generated mocks object of the test library writes a `.gcda`, but only objects built with `--coverage` write notes. Component scopes run without `GCOV_PREFIX` and are not affected; gtest is not affected because its mocks are C++. With that one `.gcda` removed, gcovr writes the variant's pytest coverage (51.7% of lines, six files). I would fix it in yanga (YANGA-013): build `<scope>_binding_mocks.c` without coverage instrumentation, or let gcovr search only the component object folders, because any project with coverage flags on all C objects hits it. The other choice is a SPLedY toolchain change outside this item.
  - **Answer (2026-11-24):** fixed in yanga (YANGA-013 `fb0e9a4`): the generated `<scope>_binding_mocks.c` and the `mockup_sources` build without coverage instrumentation. The human approved: "Yes, both fixes".
- **clanguru `bind` cannot read `uint8_t` on macOS (CLG-019).** libclang reports `'stdint.h' file not found` with the gcc compile database, which has no `-isysroot`, so `RGBColor` reads as an anonymous struct and `RteSetLightValue`, `RteGetLightValue` and `OFF_COLOR` get no binding. I worked around it with a C fake `components/light_controller/test/rte_set_light_value_fake.c` and tests that do not read the light value. I would fix it in clanguru (add the SDK sysroot on macOS when the command has none), then let the tests check the light colour as gtest does.
  - **Answer (2026-11-24):** fixed in clanguru (CLG-019 `829e197`): on macOS the parser finds the system headers with a gcc compile database. Drop the C fake and check the light colour. The human approved: "Yes, both fixes".
