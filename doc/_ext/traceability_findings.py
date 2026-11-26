"""
The ``traceability-findings`` directive: the findings of the sphinx-needs schema rules as a table.

sphinx-needs writes its findings to ``schema_violations.json`` in the output folder when writing starts,
before any page is written, but has no directive that shows them. This directive places a node that is
filled from that file when its page is written. It never fails the build.
"""

import json
import re
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective

from sphinx_needs.api import get_needs_view

FINDINGS_FILE = "schema_violations.json"
SEVERITY_ORDER = ("violation", "warning", "info")
NO_FINDINGS = "No findings: every need of this report satisfies the traceability rules."


@dataclass(frozen=True)
class Finding:
    need: str
    rule: str
    severity: str
    message: str


def rule_name(schema_path: str) -> str:
    """
    The rule of a finding: the findings file has no field for it, only ``schema_path``,
    whose first part is the rule's ``id`` and its index (``spec-is-tested[3] > validate > ...``).
    """
    return re.sub(r"\[\d+\]$", "", schema_path.split(" > ")[0])


def read_findings(report: dict[str, Any]) -> list[Finding]:
    """The top-level findings of a findings file, most severe first."""
    findings = [
        Finding(
            need=need,
            rule=rule_name(warning["details"]["schema_path"]),
            severity=warning["details"]["severity"],
            message=warning["details"].get("user_msg") or warning["details"].get("validation_msg", ""),
        )
        for need, warnings in report.get("validation_warnings", {}).items()
        for warning in warnings
    ]
    return sorted(findings, key=lambda f: (SEVERITY_ORDER.index(f.severity) if f.severity in SEVERITY_ORDER else len(SEVERITY_ORDER), f.rule, f.need))


def _table(header: list[str], rows: list[list[nodes.Node]]) -> nodes.table:
    group = nodes.tgroup(cols=len(header))
    group += [nodes.colspec(colwidth=1) for _ in header]
    group += nodes.thead("", nodes.row("", *[nodes.entry("", nodes.paragraph(text=title)) for title in header]))
    group += nodes.tbody("", *[nodes.row("", *[nodes.entry("", cell) for cell in row]) for row in rows])
    return nodes.table("", group)


def render(findings: list[Finding], need_link: Callable[[str], nodes.Node], need_type: Callable[[str], str]) -> list[nodes.Node]:
    """The count per rule and the table of findings, or the "no findings" line."""
    if not findings:
        return [nodes.paragraph(text=NO_FINDINGS)]
    counts = Counter(finding.rule for finding in findings)
    return [
        _table(["Rule", "Findings"], [[nodes.paragraph(text=rule), nodes.paragraph(text=str(count))] for rule, count in sorted(counts.items())]),
        _table(
            ["Need", "Type", "Rule", "Severity", "Message"],
            [
                [
                    nodes.paragraph("", "", need_link(finding.need)),
                    nodes.paragraph(text=need_type(finding.need)),
                    nodes.paragraph(text=finding.rule),
                    nodes.paragraph(text=finding.severity),
                    nodes.paragraph(text=finding.message),
                ]
                for finding in findings
            ],
        ),
    ]


class traceability_findings(nodes.General, nodes.Element):
    """Filled with the findings when its page is written."""


class TraceabilityFindingsDirective(SphinxDirective):
    def run(self) -> list[nodes.Node]:
        # The file is rewritten in every build, so the page is read again and shows the current findings.
        self.env.note_dependency(str(Path(self.env.app.outdir) / FINDINGS_FILE))
        return [traceability_findings()]


def fill_findings(app: Sphinx, doctree: nodes.document, docname: str) -> None:
    placeholders = list(doctree.findall(traceability_findings))
    if not placeholders:
        return
    findings_file = Path(app.outdir) / FINDINGS_FILE
    findings = read_findings(json.loads(findings_file.read_text(encoding="utf-8"))) if findings_file.is_file() else []
    needs = get_needs_view(app)

    def need_link(need_id: str) -> nodes.Node:
        need = needs.get(need_id)
        if not need or not need["docname"]:
            return nodes.Text(need_id)
        uri = f"{app.builder.get_relative_uri(docname, need['docname'])}#{need_id}"
        return nodes.reference("", need_id, refuri=uri, internal=True)

    def need_type(need_id: str) -> str:
        need = needs.get(need_id)
        return need["type_name"] if need else ""

    for placeholder in placeholders:
        placeholder.replace_self(render(findings, need_link, need_type))


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_node(traceability_findings)
    app.add_directive("traceability-findings", TraceabilityFindingsDirective)
    app.connect("doctree-resolved", fill_findings)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
