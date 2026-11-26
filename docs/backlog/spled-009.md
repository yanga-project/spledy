---
status: Open
priority: Medium
blocked_by: [SPLED-007]
---

# [SPLED-009] Full trace chain for the blinking feature, from customer requirement to test result

## Summary

As someone who develops a product line, I want SPLedY to show one feature traced from the customer requirement down to the test results, including the hazard the feature brings and the safety goal against it, so that I can see how a product line keeps every work product an assessment asks for as code, checked in every variant's build.

## Description

SPLedY's reports have good traceability at the unit level: detailed design specs, implementations, unit test specs and their gtest results are sphinx-needs items with links. Above that there is nothing to link to. The customer requirements page is plain text with repeated IDs, the software architecture page is a diagram and two tables, and there are no software requirements, no hazard analysis, no safety goals and no test specifications above the unit level. Both pages were written as placeholders.

This item builds the full chain for one feature, `BLINKING`, as a thin slice. It sets the need types, the link names, the page structure and the checks that later items reuse for the other features. `BLINKING` fits because only Disco selects it: the Disco report must show the whole chain, and the Sleep and Spa reports must show none of it.

The direction and the reasoning are in the vault idea `spledy-full-traceability-demo`.

## Scope decisions

- **Levels and their links.** The main chain is customer requirement, feature, software requirement, architecture element, detailed design (the existing `spec`), implementation, unit test spec, variant test spec, test result. Hazard analysis is a side branch, not a step every requirement passes: a feature can bring a hazard, and a hazard gets a safety goal. A software requirement links up to a feature (a functional requirement) or to a safety goal (a safety requirement); `BLINKING` gets one of each. Each level is a sphinx-needs item, and each link points up the chain. Reason: these are the work products every serious project has, in any industry.
- **Neutral names, no standard in the pages.** Types and pages use the names above, not the IDs or terms of one standard. The comments in `conf.py` that cite Automotive SPICE base practices are reworded to name the levels only. A mapping to a standard (an IEC 61508 example) belongs to the yanga-project process description, not to this item.
- **A feature is a need.** The KConfig symbol `BLINKING` gets one need that links to the customer requirements it satisfies. It is written by hand for now; generating feature needs from KConfig is a later item.
- **Variability through Jinja, as for the specs today.** Every need of the chain that only Disco has sits inside a feature condition. No explicit link from a need to its feature for filtering.
- **arc42 for the architecture.** The architecture follows the arc42 sections. This item fills only what the slice needs: section 5 (building block view) with `light_controller` and the interface it reads the knob value from. Section 5 appears in the SPL documentation report with every component and in the variant report with the selected components only.
- **The placeholder pages are replaced, not kept beside the new ones.** The new customer requirements page and the arc42 page hold only the slice's content; the other features follow in later items. Reason: the placeholders were never meant to be correct, and two architecture pages in one report would confuse the reader.
- **The hazard is real, its numbers sourced.** The hazard for a blinking light is a flash rate that can trigger photosensitive seizures; its safety goal limits the blink rate. The limit comes from a published guideline, cited in the need, not from memory.
- **The test spec above the unit is a variant test.** One test of the Disco variant test suite gets a test spec that tests the software requirement and links to its result, with the same title rule as the unit test specs.
- **The checks extend SPLED-007's rules.** Each new link gets a schema rule in the style SPLED-007 sets: missing upward link and wrong level, with the same severities. That is why this item waits for SPLED-007.
- **Most of the slice is fully traced, a few gaps are left on purpose.** One or two needs of the slice miss an upward link, so the traceability page shows what a finding looks like. Each gap has a source comment at its need saying it is on purpose, so nobody fixes it by accident. Everything else is fully traced.

## Out of scope

- The other features (`BRIGHTNESS_ADJUSTMENT`, colours) and the other arc42 sections.
- Component and feature usage tables in the SPL overview: they need data in the variant manifests from yanga-core, a separate item.
- Generating feature or architecture needs from KConfig or `components/yanga.yaml`.
- Security analysis, hardware and system level work products.
- A mapping page to any standard.

## Acceptance criteria

- [ ] The Disco gtest variant report shows one need of each level for `BLINKING` (two software requirements, one functional and one safety), checked by their IDs in the built HTML. Their links are checked by the schema rules (see the traceability criterion below).
- [ ] The Sleep and Spa gtest variant reports show none of the needs that belong only to `BLINKING`, checked by their IDs in the built HTML.
- [ ] The variant test spec of the slice links to at least one test result in the Disco report, checked by the existing schema rule that a test spec has a result.
- [ ] The SPLED-007 traceability page of the Disco report shows a finding for each gap left on purpose and no other finding for the new levels, checked by a test. So every other need of the slice has the upward links of the Levels decision.
- [ ] The customer requirements are needs with unique IDs, and the software architecture page uses the arc42 section names, checked by reading the SPL documentation report.
- [ ] `pytest test` passes.
