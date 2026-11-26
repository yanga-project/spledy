# Check the traceability of a report

Every variant report and every component report has a Traceability Report page. It lists the needs of
that report that break a traceability rule, with the need, its type, the rule, the severity and the
rule's message, and a count per rule. A report without findings says so.

The rules are sphinx-needs schema rules in `conf.py` (`needs_schema_definitions`). They follow the
trace model of the product line documentation (`doc/trace_model.md`):

- `test-results-required` (violation): a unit or variant test spec has at least one test result.
- `test-traces-to-spec` (violation): a test spec tests at least one spec, and its `tests` links point only to specs.
- `impl-traces-to-spec` (violation): an implementation implements at least one spec, and its `implements` links point only to specs.
- `spec-is-tested` (warning): a spec is tested by at least one test spec.
- `spec-is-implemented` (warning): a spec is implemented by at least one implementation.
- `hazard-arises-from-req` (violation): a hazard arises from at least one software requirement (a function), and only from those.
- `safetygoal-mitigates-hazard` (violation): a safety goal mitigates at least one hazard, and only hazards.
- `req-satisfies-custreq-or-safetygoal` (violation): a software requirement satisfies at least one customer requirement or safety goal, and only those.
- `arch-realises-req` (violation): an architecture element realises at least one software requirement, and only software requirements.
- `spec-refines-arch` (warning): a spec refines at least one architecture element, and only architecture elements.
- `spec-realises-only-req` (violation): a spec that realises something realises only software requirements.
- `vtest-traces-to-req` (violation): a variant test spec tests at least one software requirement, and only software requirements.
- `req-is-tested` (warning): a software requirement is tested by at least one variant test spec.

Each report is its own Sphinx build, so a page shows the findings of exactly that variant or component.
A spec that is tested only behind a feature the variant does not select shows up in that variant's
report only.

Findings never fail the build. sphinx-needs logs them and writes them to `schema_violations.json` in the
report's output folder; the `traceability-findings` directive (`doc/_ext/traceability_findings.py`) reads
that file and renders the page. The product line documentation report has no Traceability Report page.

To add a rule, add an entry with an `id` to `needs_schema_definitions`. The page reads the rule's name
from the `id`, so give every rule one.
