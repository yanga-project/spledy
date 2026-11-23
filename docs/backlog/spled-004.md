---
status: Done (2026-11-23)
priority: Medium
blocked_by: [YANGA-009, YCORE-004]
related: [SPLED-001, SPLED-003]
---

# [SPLED-004] Report cleanup: code host links, components by folder, readable test results

## Summary

As a reader of the SPLedY reports, I want sources and commits to link to the repository on CI, the components shown by their folder with the containers listed apart, test results that are easy to reach, and no stale pages, so that the published reports are easy to navigate and point to the right code.

## Description

Found in the published report of develop:

- The Zephyr variant reports have no source links: the Zephyr platforms do not switch source links on, and the Zephyr pipeline has no CI context, so it always counts as local. On gtest, test sources have no link on CI.
- The SPL overview shows the commit as a plain hash, and its footer links to the old repository `cuinixam/SPLed`.
- The components page is one flat list, and the container `light_application` shows as an empty chapter.
- A test result shows a "links outgoing" entry, which is only the link to its suite and file. Jumping to a result near the end of a page leaves it low on the screen.
- The hand-written CI pipeline page is out of date.
- The macOS linker troubleshooting is a heading in the Platforms chapter, so it shows in the navigation as if it were a platform.

## Scope decisions

- **Code host links on CI only**: the gtest and Zephyr platforms use yanga's `repository` strategy in the `ci` profile (gtest after `gcovr`); locally they keep `vscode`. The URL is detected from the checkout, nothing is configured.
- **The overview commit links to the commit page** of the detected repository; the footer links use the detected repository too.
- **Components as a folder tree** by their path relative to the project root (YCORE-004). **Containers in a separate list**, each with the names of its subcomponents, so no container is an empty chapter.
- **"links outgoing" is renamed** to say the result is part of its suite.
- **A bottom spacer** lets a jump place any result at the top of the window.
- **The CI pipeline page is deleted** with its references; the macOS troubleshooting moves to `doc/how-to/`.
- Out of scope: the yanga and yanga-core changes themselves (YANGA-009, YCORE-004), the coverage page grouping (YANGA-006).

## Acceptance criteria

- [x] On CI, the Zephyr and gtest source pages, test sources included, link to the repository at the build's commit; a local build links to the local files as before
- [x] The SPL overview links the commit and the footer to the detected repository
- [x] The components page shows the components in a folder tree by their path, and a separate list of containers with their subcomponents; no container is an empty chapter
- [x] A test result no longer shows "links outgoing"
- [x] A jump to the last test result on a page shows it at the top of the window
- [x] The report has no CI pipeline page and no link to it
- [x] The macOS troubleshooting is a how-to and no longer in the Platforms navigation
- [x] `pytest test` passes with the released yanga and yanga-core

## Handoff

- Intent: report cleanup for SB-008 (code host links on CI, components by folder, readable test results, no stale pages).
- Verified: `.venv/bin/python -m pytest test` with the released yanga 2.50.0, yanga-core 0.18.0 and clanguru 0.25.0 from the lock, on a clean build tree: 38 passed, 5 skipped (Arduino and zephyr_sim, not on macOS). AC 5 checked by hand in a browser.
- State: AC 2 to 8 ticked. AC 1 needs a CI run: locally the source pages link to VS Code; the CI branch of `test_source_docs_link_to_vscode_locally_and_to_the_repository_on_ci` runs only on CI.
- Next step: tick AC 1 on the first green CI run of develop, which closes the item.
- Known problems: `jarvis floor-guard` reports the replaced test `test_gtest_test_source_docs_link_to_vscode_locally_and_plain_text_on_ci`; its CI branch checked plain text, which AC 1 replaces with repository links.
