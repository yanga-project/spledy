---
status: Done (2026-11-22)
priority: Medium
blocked_by: [YANGA-011, YCORE-005]
related: [SPLED-004]
---

# [SPLED-006] Report structure from tags

## Summary

As a reader of the SPLedY reports, I want each variant report ordered as requirements, architecture, components, containers, feature configuration, reports and the rest, with the product line pages in the product line documentation, so that I find each result where I expect it and every variant report holds only what belongs to the variant.

## Description

The variant report lists generated entries in registration order, with two coverage pages a reader cannot tell apart, and repeats the platform pages of the whole product line in every variant. The SPL overview shows the product line documentation only as a small link next to the commit. With the tags of YCORE-005 and YANGA-011, the project's templates can place every entry.

## Scope decisions

- **Variant report order**: Requirements, Software Architecture, Components (by path), Containers, Feature Configuration, Reports (All components, All containers, Variant, Overall), then the untagged entries (build targets, object dependencies) in registration order. Groups without entries are left out.
- **Software Architecture stays in the variant report**, because it may depend on the selected features.
- **The platform pages move to the product line documentation report.**
- **The SPL overview shows the product line documentation in its own section** above the variant cards, titled "Product line documentation".
- **The SPL overview variant cards show no feature list** (decided 2026-11-22): the template drops the "Features" label and chips; the overview data keeps the features.
- **Each component's and container's pages are ordered by kind** (decided 2026-11-22), the same on every platform: design, sources, test results, coverage, static analysis, then the rest.
- Out of scope: a chapter for platform components (needs a `platform` tag), new requirements content.

## Acceptance criteria

- [x] The Disco gtest variant report has the order above, with no empty group
- [x] Each component chapter shows only that component's entries, and each container chapter only that container's
- [x] The Reports chapter shows All components, All containers, Variant and Overall, and no separate "Variant Test Coverage" or "Coverage Report" entry remains
- [x] The platform pages appear in the product line documentation report and in no variant report
- [x] The SPL overview shows "Product line documentation" as its own section above the variant cards
- [x] `pytest test` passes with yanga and yanga-core installed from their branches
