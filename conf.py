# -*- coding: utf-8 -*-
"""Configuration"""

import datetime
import sys
from pathlib import Path
from typing import Any

from yanga_core.docs.sphinx import SphinxConfig

day = datetime.date.today()

# meta data #################################################################

project = "SPLed"
copyright = f"{day.year}, RMT and Friends"
release = f"{day}"

# file handling #############################################################
# @see https://www.sphinx-doc.org/en/master/usage/configuration.html

templates_path = [
    "doc/_tmpl",
]

exclude_patterns = [
    "README.md",
    "build/modules",
    "build/deps",
    ".venv",
    ".git",
    "**/test_results.rst",  # We renamed this file, but nobody deletes it.
]

html_context: dict[str, Any] = {
    "env": {
        # Add current execution time in UTC
        "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    },
    # TODO: the feature configuration is not yet implemented
    "config": {},
}

include_patterns = ["index.md", "doc/**"]

report_config = SphinxConfig()
# The platform pages and the trace model describe the whole product line, so only the product line report has them.
if report_config.report_data and not report_config.report_data.has_spl_scope:
    exclude_patterns.extend(["doc/platforms/**", "doc/trace_model.md"])
# The traceability findings and the variant tests belong to one variant or component, so the product line report leaves them out.
if report_config.report_data and report_config.report_data.has_spl_scope:
    exclude_patterns.extend(["doc/traceability.md", "doc/variant_tests/**"])
html_context.update(report_config.html_context)
include_patterns.extend(report_config.include_patterns)

# Print all include patterns
print("Include patterns:")
for pattern in include_patterns:
    print(f" - {pattern}")

project = report_config.project

# configuration of built-in stuff ###########################################
# @see https://www.sphinx-doc.org/en/master/usage/configuration.html

numfig = True

# html config ###############################################################
# @see https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Omit "documentation" in title
html_title = f"{project} {release}"

html_theme = "sphinx_rtd_theme"

# Show hyper link which leeds to the source of page displayed
html_show_sourcelink = True

html_theme_options = {
    "canonical_url": "",
    "analytics_id": "",  # Provided by Google in your dashboard
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
    "logo_only": False,
    "style_nav_header_background": "white",
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 6,
    "includehidden": True,
    "titles_only": False,
}


html_logo = "doc/_figures/SPLED_logo.png"

# The bottom spacer lets a jump put any test result, also the last on a page, at the top of the window.
html_static_path = ["doc/_static"]
html_css_files = ["bottom_spacer.css"]

# extensions and their configuration #########################################
extensions = []

extensions.append("sphinx_rtd_size")
sphinx_rtd_size_width = "90%"

extensions.append("sphinxcontrib.mermaid")

# Parse markdown files
extensions.append("myst_parser")
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_admonition",
    "html_image",
]
# MyST drops links with unknown schemes; yanga resolves the `source:` links after the build.
myst_url_schemes = ["http", "https", "mailto", "ftp", "source"]

# Traceability extension
extensions.append("sphinx_needs")
extensions.append("sphinx_test_reports")
# Test specs in the docstrings of pytest test functions, titled `<module>.<function>`.
extensions.append("yanga.sphinx_pytest")
# The Traceability Report page: the findings of the schema rules below.
sys.path.insert(0, str(Path(__file__).parent / "doc/_ext"))
extensions.append("traceability_findings")

# needs_types - this option allows the setup of own need types like bugs, user_stories and more.
# The kinds of work products and their links (doc/trace_model.md). A feature has no trace links: the feature
# model is built from the customer requirements, and its conditions switch the other work products.
needs_types = [
    dict(directive="custreq", title="Customer Requirement", prefix="CR_", color="#C9D6EA", style="node"),
    dict(directive="feature", title="Feature", prefix="FEAT_", color="#D5E8D4", style="node"),
    dict(directive="hazard", title="Hazard", prefix="HAZ_", color="#F8CECC", style="node"),
    dict(directive="safetygoal", title="Safety Goal", prefix="SG_", color="#FFE6CC", style="node"),
    dict(directive="req", title="Software Requirement", prefix="R_", color="#BFD8D2", style="node"),
    dict(directive="arch", title="Architecture Element", prefix="A_", color="#E1D5E7", style="node"),
    dict(
        directive="spec",
        title="Specification",
        prefix="S_",
        color="#FEDCD2",
        style="node",
    ),
    dict(
        directive="impl",
        title="Implementation",
        prefix="I_",
        color="#DF744A",
        style="node",
    ),
    dict(directive="test", title="Test Case", prefix="T_", color="#DCB239", style="node"),
    dict(directive="vtest", title="Variant Test Spec", prefix="VT_", color="#F5E6A3", style="node"),
]

# Define own link types
needs_links = {
    # sphinx-test-reports links a test result to its suite and its file with the default link type.
    "links": {"incoming": "contains", "outgoing": "is part of"},
    # A software requirement to the customer requirement or the safety goal it satisfies.
    "satisfies": {"incoming": "is satisfied by", "outgoing": "satisfies"},
    # A hazard to the function (software requirement) it arises from.
    "arises_from": {"incoming": "brings", "outgoing": "arises from"},
    # A safety goal to the hazard it mitigates.
    "mitigates": {"incoming": "is mitigated by", "outgoing": "mitigates"},
    # An architecture element, or a spec that covers a requirement inside one component, to the software
    # requirements it realises.
    "realises": {"incoming": "is realised by", "outgoing": "realises"},
    # A detailed design spec to the architecture element it refines.
    "refines": {"incoming": "is refined by", "outgoing": "refines"},
    # An implementation to the detailed design spec it implements.
    "implements": {"incoming": "is implemented by", "outgoing": "implements"},
    # A unit test spec to a detailed design spec; a variant test spec to a software requirement.
    "tests": {"incoming": "is tested by", "outgoing": "tests"},
    # A test spec to its test results.
    # A test spec titled `Suite.Case` (clanguru's `{{ gtest.test }}`) links every gtest result of that test.
    # The rule drops the `Prefix/` of a parametrized suite and the `/N` of each instance, so a TEST_P spec needs no pattern.
    "results": {
        "incoming": "is resulted from",
        "outgoing": "results",
        "default": (
            "[[links_from_filter(\"type == 'testcase'"
            " and current_need['title'].split('.')[0] in classname.split('/')"
            " and case.split('/')[0] == current_need['title'].split('.')[1]"
            # A pytest spec titled `<module>.<function>` links every result of that function, parameters included.
            " or type == 'testcase' and classname == current_need['title'].rpartition('.')[0]"
            " and case.split('[')[0] == current_need['title'].rpartition('.')[2]\")]]"
        ),
    },
}

# The traceability rules. Their findings are logged, written to schema_violations.json and shown on the
# Traceability Report page; they never fail the build, because yanga builds without `-W`.
SPEC = {"local": {"properties": {"type": {"const": "spec"}}}}
TEST = {"local": {"properties": {"type": {"const": "test"}}}}
IMPL = {"local": {"properties": {"type": {"const": "impl"}}}}
HAZARD = {"local": {"properties": {"type": {"const": "hazard"}}}}
CUSTREQ_OR_SAFETYGOAL = {"local": {"properties": {"type": {"enum": ["custreq", "safetygoal"]}}}}
REQ = {"local": {"properties": {"type": {"const": "req"}}}}
ARCH = {"local": {"properties": {"type": {"const": "arch"}}}}
VTEST = {"local": {"properties": {"type": {"const": "vtest"}}}}


def traces_up(rule_id: str, need_type: str, link: str, target: dict[str, Any], severity: str = "violation") -> dict[str, Any]:
    """A need of this type has at least one link of this kind, and every one points to the level above."""
    return {
        "id": rule_id,
        "severity": severity,
        "select": {"properties": {"type": {"const": need_type}}},
        "validate": {"network": {link: {"items": target, "contains": target, "minContains": 1}}},
    }


needs_schema_definitions = {
    "schemas": [
        {
            # A typo in the title or a test that did not run leaves a test spec without a result.
            "id": "test-results-required",
            "select": {"properties": {"type": {"enum": ["test", "vtest"]}}},
            "validate": {"local": {"properties": {"results": {"minItems": 1}}, "required": ["results"]}},
        },
        {
            "id": "test-traces-to-spec",
            "select": {"properties": {"type": {"const": "test"}}},
            "validate": {"network": {"tests": {"items": SPEC, "contains": SPEC, "minContains": 1}}},
        },
        {
            "id": "impl-traces-to-spec",
            "select": {"properties": {"type": {"const": "impl"}}},
            "validate": {"network": {"implements": {"items": SPEC, "contains": SPEC, "minContains": 1}}},
        },
        {
            "id": "spec-is-tested",
            "severity": "warning",
            "select": {"properties": {"type": {"const": "spec"}}},
            "validate": {"network_back": {"tests": {"contains": TEST, "minContains": 1}}},
        },
        {
            "id": "spec-is-implemented",
            "severity": "warning",
            "select": {"properties": {"type": {"const": "spec"}}},
            "validate": {"network_back": {"implements": {"contains": IMPL, "minContains": 1}}},
        },
        traces_up("hazard-arises-from-req", "hazard", "arises_from", REQ),
        traces_up("safetygoal-mitigates-hazard", "safetygoal", "mitigates", HAZARD),
        traces_up("req-satisfies-custreq-or-safetygoal", "req", "satisfies", CUSTREQ_OR_SAFETYGOAL),
        traces_up("arch-realises-req", "arch", "realises", REQ),
        # A warning: most specs do not refine an architecture element yet, and each later feature item adds them.
        traces_up("spec-refines-arch", "spec", "refines", ARCH, severity="warning"),
        {
            # A spec may also realise a software requirement directly; if it does, only software requirements.
            "id": "spec-realises-only-req",
            "select": {"properties": {"type": {"const": "spec"}}},
            "validate": {"network": {"realises": {"items": REQ}}},
        },
        traces_up("vtest-traces-to-req", "vtest", "tests", REQ),
        {
            "id": "req-is-tested",
            "severity": "warning",
            "select": {"properties": {"type": {"const": "req"}}},
            "validate": {"network_back": {"tests": {"contains": VTEST, "minContains": 1}}},
        },
    ]
}

# The suffix of source filenames.
source_suffix = [
    ".md",
    ".rst",
]


def setup(app):  # type: ignore
    app.connect("source-read", report_config.render_with_jinja)
