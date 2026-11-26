---
status: Done (2026-11-26)
priority: Medium
blocked_by: [SPLED-007]
---

# [SPLED-009] Full trace chain for the blinking feature, from customer requirement to test result

## Summary

As someone who develops a product line, I want SPLedY to show one feature traced from the customer requirement down to the test results, including the hazard the blinking function brings and the safety goal against it, so that I can see how a product line keeps every work product an assessment asks for as code, checked in every variant's build.

## Description

SPLedY's reports have good traceability at the unit level: detailed design specs, implementations, unit test specs and their gtest results are sphinx-needs items with links. Above that there is nothing to link to. The customer requirements page is plain text with repeated IDs, the software architecture page is a diagram and two tables, and there are no software requirements, no hazard analysis, no safety goals and no test specifications above the unit level. Both pages were written as placeholders.

This item builds the full chain for one feature, `BLINKING`, as a thin slice. It sets the need types, the link names, the page structure and the checks that later items reuse for the other features. `BLINKING` fits because only Disco selects it: the Disco report must show the whole chain, and the Sleep and Spa reports must show none of it.

The direction and the reasoning are in the vault idea `spledy-full-traceability-demo`.

## Scope decisions

- **Levels and their links, as the Trace Model page draws them.** The main chain is customer requirement, software requirement, architecture element, detailed design (the existing `spec`), implementation, unit test spec, variant test spec, test result. Hazard analysis is a side branch, not a step every requirement passes: a function (a software requirement) can bring a hazard, and a hazard gets a safety goal. A software requirement links up to a customer requirement (a functional requirement) or to a safety goal (a safety requirement); blinking gets one of each. A feature is not a level of the chain and has no trace links (decided by the human, 2026-11-26): the feature model is built from the customer requirements and holds a feature only where customers differ; its conditions switch every kind of work product except the customer requirements. Each level is a sphinx-needs item, and each link points up the chain. Reason: these are the work products every serious project has, in any industry.
- **Neutral names, no standard in the pages.** Types and pages use the names above, not the IDs or terms of one standard. The comments in `conf.py` that cite Automotive SPICE base practices are reworded to name the levels only. A mapping to a standard (an IEC 61508 example) belongs to the yanga-project process description, not to this item.
- **A feature is a need without links.** The KConfig symbol `BLINKING` gets one need that describes it and names its definition in `KConfig`. It is written by hand for now; generating feature needs from KConfig is a later item.
- **Variability through Jinja, as for the specs today.** Every need of the chain that only Disco has sits inside a feature condition. No explicit link from a need to its feature for filtering.
- **arc42 for the architecture.** The architecture follows the arc42 sections. This item fills only what the slice needs: section 5 (building block view) with `light_controller` and the interface it reads the knob value from. Section 5 appears in the SPL documentation report with every component and in the variant report with the selected components only.
- **The placeholder pages are replaced, not kept beside the new ones.** The new customer requirements page and the arc42 page hold only the slice's content; the other features follow in later items. Reason: the placeholders were never meant to be correct, and two architecture pages in one report would confuse the reader.
- **The hazard is real, its numbers sourced.** The hazard for a blinking light is a flash rate that can trigger photosensitive seizures; its safety goal limits the blink rate. The limit comes from a published guideline, cited in the need, not from memory.
- **The test spec above the unit is a variant test.** One test of the Disco variant test suite gets a test spec that tests the software requirement and links to its result, with the same title rule as the unit test specs.
- **The checks extend SPLED-007's rules.** Each new link gets a schema rule in the style SPLED-007 sets: missing upward link and wrong level, with the same severities. That is why this item waits for SPLED-007.
- **Most of the slice is fully traced, a few gaps are left on purpose.** One or two needs of the slice miss an upward link, so the traceability page shows what a finding looks like. Each gap has a source comment at its need saying it is on purpose, so nobody fixes it by accident. Everything else is fully traced.
- **The rule that a spec refines an architecture element covers every spec, as a warning.** In this slice only the specs of the blinking chain refine an architecture element, so the other specs show a warning each on the Traceability Report page. Reason (decided by the human, 2026-11-26): the page shows the real state of the product line, and the later items for the other features remove those warnings one by one.

## Out of scope

- The other features (`BRIGHTNESS_ADJUSTMENT`, colours) and the other arc42 sections.
- Component and feature usage tables in the SPL overview: they need data in the variant manifests from yanga-core, a separate item.
- Generating feature or architecture needs from KConfig or `components/yanga.yaml`.
- Security analysis, hardware and system level work products.
- A mapping page to any standard.

## What users see

- **New need types and links in `conf.py`.** Types: customer requirement, feature, hazard, safety goal, software requirement (the unused `req` type becomes it), architecture element and variant test spec; `spec`, `impl` and `test` stay. Links: `satisfies` (software requirement to customer requirement or safety goal), `arises_from` (hazard to software requirement), `mitigates` (safety goal to hazard), `realises` (architecture element to software requirement, and a spec to a software requirement that lies inside one component), `refines` (spec to architecture element); the variant test spec uses the existing `tests` and `results`. Not breaking: existing needs keep their links. UAT: no, covered by the pages below. Why: sphinx-needs knows only the types and links a project declares. Approved by the human (2026-11-26)
- **The product line documentation and the variant reports get new chapters:** Customer Requirements (replaced), Features, Hazard Analysis, Software Requirements, Software Architecture (replaced, arc42 section 5 only) and, in the product line documentation only, Trace Model (the kinds of work products and their links). Breaking for readers of the old placeholder pages, which go away. UAT: yes, the Disco variant report and the product line documentation. Why: the placeholders hold no needs to link to. Approved by the human (2026-11-26)
- **The fastest blink of a blinking variant gets slower.** Today the light switches every 10 task cycles of 10 ms, which is 5 flashes per second at the knob's top position; the safety requirement allows at most 3 (WCAG 2.2, success criterion 2.3.1). The minimum blink period rises to 170 ms. Breaking: Disco blinks visibly slower at the top knob positions. UAT: yes, on `pc_gui`. Why: the safety goal is only true if the code meets it. Approved by the human (2026-11-26)
- **More findings on the Traceability Report page**, from the rules of the new links and the gaps left on purpose. Not breaking: findings never fail the build. UAT: no, covered by the variant test. Why: the page is how a reader sees the gaps. Approved by the human (2026-11-26)

## Acceptance criteria

- [x] The Disco gtest variant report shows one need of each level for `BLINKING` (two software requirements, one functional and one safety), checked by their IDs in the built HTML. Their links are checked by the schema rules (see the traceability criterion below).
- [x] The Sleep and Spa gtest variant reports show none of the needs that belong only to `BLINKING`, checked by their IDs in the built HTML.
- [x] The variant test spec of the slice links to at least one test result in the Disco report, checked by the existing schema rule that a test spec has a result.
- [x] The SPLED-007 traceability page of the Disco report shows a finding for each gap left on purpose and no other finding for the new levels, checked by a test. So every other need of the slice has the upward links of the Levels decision.
- [x] The customer requirements are needs with unique IDs, and the software architecture page uses the arc42 section names, checked by reading the SPL documentation report.
- [x] `pytest test` passes.
- [x] UAT: the human reads the chain for `BLINKING` in the Disco variant report and in the product line documentation, and sees the slower fastest blink on `pc_gui`.

## Plan

1. `conf.py`: the need types and links of What users see, the ASPICE comments reworded to name the levels, and one schema rule per new link (missing upward link `violation`, wrong level by `items` on that link field), plus `swreq-is-tested` (`warning`: a software requirement is tested by a variant test spec). Check: a Disco report build writes the rules into `schema_violations.json`.
2. Customer requirements: `doc/customer_requirements/index.md` replaced by needs; for this slice the Disco customer's requirement for a blinking light, inside the `BLINKING` condition. Check: unique IDs, built in the product line documentation.
3. `doc/features/index.md`: the `BLINKING` feature need, written by hand, with no trace links, carries a `source:` link to the `config BLINKING` line of `KConfig`; inside the `BLINKING` condition in the variant report and always in the product line documentation.
4. `doc/hazard_analysis/index.md`: the hazard "flashing light triggers a photosensitive seizure" `arises_from` the functional software requirement, and the safety goal "the light flashes at most 3 times in any one second" `mitigates` it, citing WCAG 2.2 SC 2.3.1 by URL. The guideline is written for screens; applying it to a lamp is our inference, said in the need.
5. `doc/software_requirements/index.md`: one functional requirement (the blink period follows the main knob) `satisfies` the customer requirement, one safety requirement (the light toggles no faster than every 170 ms) `satisfies` the safety goal.
6. `doc/software_architecture/index.md`: replaced by arc42 section 5, building block view, with the `light_controller` component and the `RteGetMainKnobValue` interface as architecture elements that `realise` the two software requirements. In the product line documentation every component of the pool is listed; in the variant report only the selected ones.
7. `components/light_controller`: `SWDD_LC-101` and `-203` `refine` the architecture elements; a new spec for the minimum blink period, which also `realises` the safety requirement directly; `calculateBlinkPeriod` keeps at least 170 ms, computed from `CONFIG_OS_TASK_PERIOD`; the unit tests follow the new minimum (gtest and pytest).
8. `variants/Disco/test_disco_variant.py`: a variant test that turns the knob to 100 and counts the light changes over one second, with a test spec in its docstring that `tests` the safety requirement and links its result.
9. Gaps on purpose: the functional software requirement gets no variant test, so `swreq-is-tested` reports it; a source comment at the need says it is on purpose.
10. `test/test_Disco.py`, `test/test_Sleep.py`, `test/test_Spa.py`: the need IDs of the slice are in the Disco report HTML and in none of Sleep's or Spa's; the Disco Traceability Report page shows the gap on purpose and no other finding for the new rules; the product line documentation uses the arc42 section name. Check: `pytest test`. The human does the UATs.
