from docutils import nodes

from traceability_findings import NO_FINDINGS, Finding, read_findings, render

# A findings file as sphinx-needs 9.3 writes it, cut to the fields the page reads.
REPORT = {
    "validation_warnings": {
        "SWDD_LC-200": [
            {
                "log_lvl": "warning",
                "type": "sn_schema_warning",
                "subtype": "network_contains_too_few",
                "details": {
                    "severity": "warning",
                    "need_path": "SWDD_LC-200 > tests (incoming)",
                    "schema_path": "spec-is-tested[3] > validate > network_back > tests > contains",
                    "validation_msg": "Too few valid incoming links of type 'tests' (0 < 1)",
                },
                "children": [],
            }
        ],
        "TEST_LC-001": [
            {
                "log_lvl": "error",
                "type": "sn_schema_violation",
                "subtype": "local_fail",
                "details": {
                    "severity": "violation",
                    "need_path": "TEST_LC-001",
                    "schema_path": "test-results-required[0] > local > properties > results > minItems",
                    "validation_msg": "[] has less than 1 item",
                },
                "children": [],
            }
        ],
    }
}


def test_findings_name_their_rule_and_come_most_severe_first() -> None:
    findings = read_findings(REPORT)

    assert findings == [
        Finding("TEST_LC-001", "test-results-required", "violation", "[] has less than 1 item"),
        Finding("SWDD_LC-200", "spec-is-tested", "warning", "Too few valid incoming links of type 'tests' (0 < 1)"),
    ]


def test_no_findings_renders_the_no_findings_line() -> None:
    rendered = render(read_findings({"validation_warnings": {}}), nodes.Text, lambda need: "")

    assert [node.astext() for node in rendered] == [NO_FINDINGS]


def test_findings_render_a_count_per_rule_and_one_row_per_finding() -> None:
    counts, table = render(read_findings(REPORT), nodes.Text, lambda need: "Specification")

    assert [row.astext().split("\n\n") for row in counts.findall(nodes.row)][1:] == [["spec-is-tested", "1"], ["test-results-required", "1"]]
    assert len(list(table.findall(nodes.row))) == 1 + 2
