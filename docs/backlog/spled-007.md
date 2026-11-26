---
status: Done (2026-11-26)
priority: Medium
---

# [SPLED-007] Traceability report page in the variant and component reports

## Summary

As the author of SPLedY, I want a Traceability Report page in every variant and component report so that I see missing links and links to the wrong level for exactly that variant or component. Findings never fail the build.

## Description

The variant and component reports show the sphinx-needs items and their links, but nothing checks them. A spec without a test, an implementation without a spec, or a test spec that points at an implementation instead of a spec goes unnoticed. Some gaps exist only in one variant: three light controller specs (`SWDD_LC-200` to `-202`) have no test in Disco, because their only test is behind `CONFIG_BRIGHTNESS_ADJUSTMENT_AUTOMATIC`, which Disco does not select. Only a check inside each variant's own build sees that.

sphinx-needs (9.2 and later) validates needs against schema rules during the build and writes the findings to `schema_violations.json` in the output folder, before any page is written. A page of the same build can therefore read and show them. A throwaway trial on develop showed 12 findings on unchanged sources, the wrong-level rule firing on a planted link, and a threshold giving exit 0 or 2 as set. sphinx-needs only logs the findings; it has no directive that shows them on a page, and a logged violation does not change the exit code.

## What exists

- [AGENTS.md](../../AGENTS.md): reports are built per variant and platform in `.yanga/build/<variant>/<platform>/reports/`; integration tests call `RunCommand` directly.
- [README.md](../../README.md), lines 54 to 62: the links to the how-to pages, where the new how-to gets its link.
- [conf.py](../../conf.py): the extensions (lines 116 to 119, no local extension and no import path entry yet), the need types `req`, `spec`, `impl`, `test` (lines 122 to 138), the links `links`, `implements`, `tests`, `results` (lines 142 to 165), and the `test-results-required` rule with no `severity`, so it is a violation, and a comment that says it fails the build (lines 168 to 178).
- [index.md](../../index.md): the component report (line 10, `create_component_myst_toc`), the product line documentation report (lines 12 to 25, no Reports chapter) and the variant report, which adds the Reports chapter only when merged, variant test, coverage or overall results exist (lines 49 to 51).
- [doc/reports.md](../../doc/reports.md): the Reports chapter, one toctree per report group, empty groups skipped (SPLED-006).
- [doc/how-to/](../../doc/how-to/): four how-to pages, the place for the new one.
- [pyproject.toml](../../pyproject.toml), line 15: `sphinx-needs>=9.1,<10`; `poetry.lock` holds 9.2.0.
- [test/test_Disco.py](../../test/test_Disco.py): the `test_platform_build_dir` fixture builds `report` and `light_controller_report` on the `test` platform (lines 66 to 79); the check of `reports/doc/reports.html` (lines 180 to 196) is the model for the page check.
- The repository has no decision records and no glossary.

## Scope decisions

- **Findings come from sphinx-needs schema rules in the normal Sphinx build.** No own rule engine, no separate tool.
- **The rules,** declared in `conf.py` next to the need types and links they name, each on one link field:
  - a test spec has a result: the existing `test-results-required` rule, kept as it is (`violation`). Its comment says it fails the build, which is not true today (yanga builds without `-W`); the comment is corrected;
  - a test spec traces to a spec, and its `tests` links point only to specs (`violation`);
  - an implementation traces to a spec, and its `implements` links point only to specs (`violation`);
  - a spec is tested (incoming `tests`) and is implemented (incoming `implements`) (`warning`, because they are most of the findings today).
  "Only to specs" is `items` on that one field, never on all outgoing links: test specs also carry `results` links to test cases. Missing links use `contains`/`minContains`, missing incoming links use `network_back`.
- **A small local Sphinx extension in this repository** provides a `traceability-findings` directive. The directive renders the findings for whatever rules the project declares. It is the same kind of build step as sphinx-test-reports. It may later move into sphinx-needs or a package of its own; that move is not part of this item.
- **The page is a static file**: a heading and the directive. In the variant report it is part of the Reports chapter, because the findings are a check result like coverage and static analysis; the Reports chapter is then built on every platform, with the page as its only entry where no merged, variant test, coverage or overall results exist. In the component report it follows the generated table of contents. The product line documentation report leaves the page out, as it does the platform pages. yanga and yanga-core are not changed.
- **Scope comes from the build.** Each variant and component report is its own Sphinx build, so the page shows exactly that report's needs, with no filtering.
- **Findings never fail the build.** A `traceability_fail_on` threshold was considered and dropped: a platform without tests always has untested specs, so one threshold would fail there every time. Whether the whole variant is implemented and tested is checked on a variant aggregated report that collects the data of all builds of a variant, a later item.
- **The rule name** is read from the first part of each finding's `schema_path`, because the findings file has no field for it. One test fails if sphinx-needs changes that text.
- **The sphinx-needs floor rises to 9.3** (released 2026-11-19, the current release), and the lock file follows, so every build has the schema rules this item needs.
- **Architect check (2026-11-23):**
  - `conf.py`: the rules, the extension's registration and its folder on the import path. Fits: the need types and links are declared there.
  - the local extension: the directive. Fits: a build step of this repository's reports, nothing like it exists yet.
  - the report templates (`index.md`, the Reports chapter): the page in the variant and component reports, and left out of the product line report. Fits: they are this repository's own templates.
  - `pyproject.toml` and the lock file: the sphinx-needs floor. Fits.
  - the Disco integration test: checks the page on the existing report build of the `test` platform. Fits.
  - the how-to pages: one new page. Fits.
- **Out of scope:** coverage percentages or charts, a trace graph, per-need waivers, rules across more than one level, finding counts on the SPL overview, the variant aggregated report (all builds of a variant in one report), a setting that fails the build on findings, the `Unknown option 'integrity'` warning in `power_signal_processing`.

## What users see

- **A Traceability Report page in every variant report and component report.** It lists the schema findings of that report's needs, or says there are none. Not breaking: no existing page loses content, and the build never fails on findings. UAT: yes, you read the page in the Disco report. Why: sphinx-needs only logs the findings and has no directive that shows them on a page. Approved by the human (2026-11-25)
- **The `traceability-findings` directive.** It renders the findings of the build it runs in; it never fails the build. Not breaking. UAT: no, covered by the page above. Why: sphinx-needs has no directive that shows its findings. Approved by the human (2026-11-25)
- **New schema rules for test specs, implementations and specs.** Today's sources give about 12 findings, shown on the page. Not breaking, because the build does not fail on them. UAT: no, covered by the page above. Why: without rules there are no findings to show. Approved by the human (2026-11-25)
- **The Reports chapter appears in the variant report on every platform** that builds a report, with the Traceability Report page as its only entry where no merged, variant test, coverage or overall results exist. Not breaking. UAT: no, covered by the page above. Why: the findings are a check result like coverage and static analysis, and the Reports chapter is where the variant report lists check results. Approved by the human (2026-11-25)
- **The sphinx-needs floor rises from 9.1 to 9.3.** Breaking only for an environment pinned below 9.3; the lock file follows. UAT: no. Why: 9.2 already has the schema features the rules use; 9.3 is the current release, and the floor makes every build use it. Approved by the human (2026-11-25)

## Acceptance criteria

- [x] The Disco variant report on the `test` platform and the `light_controller` component report each have a Traceability Report page that lists every finding with the need (linked), its type, the rule, the severity and the rule's message, plus a count per rule.
- [x] A report with no findings says so on its page: the extension test renders an empty findings sample and gets the "no findings" line.
- [x] The Disco report build succeeds despite findings.
- [x] The Disco variant report on `pc_terminal`, which has no test results, has a Reports chapter whose only entry is the Traceability Report page: checked in `test/test_Disco.py` on the existing `pc_terminal` report build.
- [x] A test fails when the rule name can no longer be read from the findings file.
- [x] A how-to page next to the other how-to pages describes the rules and the page.
- [x] `pytest test` passes.
- [x] UAT: the human opens the Traceability Report page of the Disco variant report and confirms that it shows the findings of that variant, including the untested `SWDD_LC-200` (`-201` and `-202` are tested by the pytest tests since SPLED-008).

## Plan

1. `pyproject.toml` and `poetry.lock`: raise the sphinx-needs floor to 9.3 and relock (poetry from the env setup script). Check: the bootstrap installs 9.3, and the Disco report build in step 2 runs on it, so the findings file layout and the `schema_path` text are checked on 9.3.
2. `conf.py`: add the rules next to the need types and links, correct the comment of `test-results-required`, put the extension folder on the import path and register the extension. Check: a Disco report build on the `test` platform writes `schema_violations.json` with the rule names of this item.
3. The local extension in `doc/`: the `traceability-findings` directive (table of findings with the linked need, type, rule, severity and message, a count per rule, or a "no findings" line). Check: a test of the extension in `test/`, built on findings samples, reads the rule name from `schema_path` and fails when that text changes, renders the "no findings" line for an empty sample.
4. Report templates: a Traceability Report page (a heading and the directive); `doc/reports.md` lists it, `index.md` shows the Reports chapter in every variant report and adds the page after the component table of contents; the product line documentation leaves it out. Check: the page appears in a Disco variant report and in one component report, and not in the SPL documentation report.
5. `doc/how-to/`: one page on the rules and the page. The README links the new how-to next to the other four.
6. `test/test_Disco.py`: on the existing report build of the `test` platform, the Disco variant report and the `light_controller` component report have the page, it lists findings with a count per rule and the build passes; the `pc_terminal` Disco report has the Reports chapter with the page as its only entry.
7. Run `pytest test`. The human does the UAT on the Disco report.
