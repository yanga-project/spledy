"""
Builds a set of variants that works on every OS, then the SPL overview from them.

Run it with `pytest test/test_spl.py`, then open `.yanga/build/index.html`.
"""

import re
import subprocess  # nosec
import sys
from pathlib import Path

import pytest

from yanga_core.commands.run import RunCommand, RunCommandConfig

BUILDS = [
    ("Disco", "test"),
    ("Disco", "pc_terminal"),
    ("Disco", "zephyr_esp32h2"),
    ("Sleep", "test"),
    ("Sleep", "pc_terminal"),
    ("Spa", "test"),
    ("Spa", "pc_gui"),
]


@pytest.fixture(scope="module")
def overview_file() -> Path:
    """Build in a fixture, so that selecting the test with `-k` still builds first."""
    project_dir = Path.cwd()
    build_dir = project_dir / ".yanga" / "build"
    # The overview lists every manifest on the disk; this run must list only its own builds.
    for manifest in (build_dir / "variants").rglob("publish_manifest.json"):
        manifest.unlink()

    for variant, platform in BUILDS:
        config = RunCommandConfig(
            project_dir=project_dir,
            platform=platform,
            variant_name=variant,
            not_interactive=True,
            target="report",
        )
        assert RunCommand().do_run(config) == 0, f"Building {variant} on {platform} failed"

    # This interpreter, because a pypeline outside the project venv cannot load the steps.
    subprocess.run([sys.executable, "-m", "pypeline.main", "run", "--config-file", "spl_pypeline.yaml"], cwd=project_dir, check=True)  # nosec
    return build_dir / "index.html"


def test_overview_links_every_build(overview_file: Path) -> None:
    # Arrange
    html = overview_file.read_text(encoding="utf-8")

    # Act
    relative_links = [href for href in re.findall(r'href="([^"]+)"', html) if "://" not in href]
    variant_links = [link for link in relative_links if link.startswith("variants/")]

    # Assert
    assert [link for link in relative_links if not (overview_file.parent / link).is_file()] == []
    assert len(variant_links) == len(BUILDS), variant_links
    for variant, platform in BUILDS:
        assert any(link.startswith(f"variants/{variant}/{platform}/") for link in variant_links), f"No link for {variant} on {platform}"
    assert 'class="commit-mismatch"' not in html, "Every build in this run must come from the current commit"


def test_overview_links_the_commit_and_the_footer_to_the_repository(overview_file: Path, repository_url: str, head_commit: str) -> None:
    # Arrange
    html = overview_file.read_text(encoding="utf-8")

    # Act
    footer_links = dict((text, href) for href, text in re.findall(r'<a\b[^>]*\bhref="([^"]+)"[^>]*>(README|Repository)</a>', html))

    # Assert
    assert f'href="{repository_url}/commit/{head_commit}"' in html, "The commit does not link to its commit page"
    assert footer_links.keys() == {"README", "Repository"}, footer_links
    assert all(href.startswith(repository_url) for href in footer_links.values()), footer_links
    assert not re.search(r"github\.com/cuinixam/SPLed\b", html), "The overview still links the old repository"


def test_product_line_documentation_has_the_platform_pages(overview_file: Path) -> None:
    # Arrange
    doc = overview_file.parent / "spl/reports"

    # Act
    index = (doc / "index.html").read_text(encoding="utf-8")
    platforms = (doc / "doc/platforms/index.html").read_text(encoding="utf-8")

    # Assert
    assert 'href="doc/platforms/index.html"' in index, "The product line documentation does not link the Platforms page"
    assert "tapi error" not in platforms, "The macOS troubleshooting is still on the Platforms page"
    assert (doc / "doc/how-to/fix-the-macos-tapi-error.html").is_file()


def test_overview_shows_the_product_line_documentation_above_the_variants(overview_file: Path) -> None:
    # Arrange
    html = overview_file.read_text(encoding="utf-8")

    # Act
    heading = re.search(r"<h[1-6]\b[^>]*>\s*Product line documentation\s*</h[1-6]>", html)

    # Assert
    assert heading, "The overview has no Product line documentation section"
    assert heading.start() < html.index('<article class="card"'), "Product line documentation is not above the variant cards"


# The needs that only a blinking variant has: the blinking chain without the light_controller component element.
BLINKING_ONLY = ["CR_DISCO-001", "FEAT_BLINKING", "HAZ_BLINK-001", "SG_BLINK-001", "SWRS_BLINK-001", "SWRS_BLINK-002", "ARCH_RTE_MAIN_KNOB", "SWDD_LC-101", "SWDD_LC-104", "VT_DISCO-001"]


@pytest.mark.parametrize("variant", ["Sleep", "Spa"])
def test_variant_without_blinking_has_none_of_the_blinking_needs(overview_file: Path, variant: str) -> None:
    # Arrange
    pages = (overview_file.parent / "variants" / variant / "test/reports").rglob("*.html")

    # Act
    ids = {need_id for page in pages for need_id in re.findall(r'\bid="([^"]+)"', page.read_text(encoding="utf-8"))}

    # Assert
    assert ids, f"No report pages for {variant}"
    assert [need for need in BLINKING_ONLY if need in ids] == []


def test_product_line_documentation_has_the_chain_and_the_arc42_section(overview_file: Path) -> None:
    # Arrange
    doc = overview_file.parent / "spl/reports/doc"

    # Act
    requirements = (doc / "customer_requirements/index.html").read_text(encoding="utf-8")
    architecture = (doc / "software_architecture/index.html").read_text(encoding="utf-8")

    # Assert
    requirement_ids = re.findall(r'\bid="(CR_[^"]+)"', requirements)
    assert requirement_ids and len(requirement_ids) == len(set(requirement_ids)), requirement_ids
    assert re.search(r"<h2\b[^>]*>5 Building Block View<", architecture), "No arc42 section 5 on the architecture page"
    assert 'id="ARCH_LC"' in architecture
    assert not (doc / "variant_tests").exists(), "The product line documentation has the variant tests"
