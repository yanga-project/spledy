# SPLED-007 fresh-reader check

## Run 1 (2026-11-25)

No `must fix` finding. The reader judged the item almost buildable.

- **1. Threshold in the integration test** (Plan step 6, AC 3; Checkable; should fix). The Disco build cannot set `traceability_fail_on`: yanga runs `sphinx-build` without `-D` and has no `yanga.yaml` field. Settled: the thresholds are checked by a test of the extension on findings samples; the Disco test checks only that the build passes with the value unset.
- **2. Two builds for "fails, else passes"** (same place; Checkable; should fix). Setting the value in the shared fixture would break the other tests. Settled by the fix of finding 1.
- **3. No report with zero findings** (AC 2; Checkable; should fix). Settled: the extension test renders an empty findings sample.
- **4. Reports chapter on every platform not listed** (What users see; Visible; should fix). Settled: added as a fifth user-visible change, waiting for the human's approval; "no existing page changes" corrected to "no existing page loses content".
- **5. ADR under `doc/` is built into every report** (Plan step 5; Placed; should fix). Settled: the ADR goes to `docs/adrs/` (folder name chosen by the human), outside the Sphinx include patterns.
- **6. How the SPL report leaves the page out** (Scope; Placed; for later). Left to the builder: exclude the page file the way `doc/platforms/**` is excluded in `conf.py`.
- **7. README link to the how-to** (What exists; Placed; should fix). Settled: added to Plan step 5.
- **8. Extension module name and file** (Plan step 3; Placed; for later). Left to the builder; `doc/generate_overall_report.py` is the precedent for Python in `doc/`.
- **9. 9.3 not checked** (Scope, What users see; Consistent; should fix). Settled: Plan step 1's check runs the step 2 build on 9.3.
- **10. Which component report** (AC 1; Checkable; for later). Settled anyway: `light_controller`, which the fixture already builds.
- **11. ADR status "Accepted" while a draft** (ADR draft; Consistent; for later). Left as is: the decision is accepted; the file lands with the implementation.

After run 1 the human dropped `traceability_fail_on`: findings never fail the build. Findings 1 and 2 above, which settled how the threshold is tested, are therefore moot.

## Run 2 (2026-11-25), changes only

No `must fix` finding.

- **1. "does not fail on findings by default"** (What users see; Consistent; should fix). Settled: "never fails on findings".
- **2. How-to still describes "the setting"** (AC, Plan step 5; Consistent; should fix). Settled: the how-to describes the rules and the page.
- **3. Architect check names a config value** (Scope; Placed; should fix). Settled: the extension holds the directive only.
- **4. The Reports chapter on every platform has no check** (Acceptance criteria; Checkable; should fix). Settled: a criterion and Plan step 6 check the `pc_terminal` Disco report, which has no test results, on the existing `pc_terminal` report build.
- **5. Wording of the fifth change** (What users see; Consistent; should fix). Settled: "every platform that builds a report", and "merged" added to the list of results, as in `index.md`.
- **6. Where the page goes in `doc/reports.md`** (Plan step 4; Placed; for later). Left to the builder: its own group or a fixed entry.

After run 2 the human moved the decision record out of this item: it is about the report tooling, not about SPLedY, and lands later in the repository that takes over the extension. Findings 5 and 11 of run 1 are therefore moot.
