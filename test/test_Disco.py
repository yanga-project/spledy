import re
import sys
from pathlib import Path
from xml.etree import ElementTree

import pytest
from pypeline_semantic_release.check_ci_context import CISystem

from spled_lib import POWER_BUTTON_KEY, Variant, build_dir, find_library
from yanga_core.commands.run import RunCommand, RunCommandConfig

VARIANT_NAME = "Disco"
# POWER_BUTTON_PRESS_DEBOUNCE, from components/power_button/src/power_button.h.
PRESS_DEBOUNCE_STEPS = 10
LIGHT_OFF = "#000000"
# CONFIG_COLOR_GREEN at the default brightness of 128.
LIGHT_GREEN = "#008000"
# A resolved `source:` link to a coverage page: href, fragment line, link text path and line.
COVERAGE_LINK = re.compile(r'<a\b[^>]*\bhref="([^"#]*coverage/[^"#]*\.html)#[lL](\d+)"[^>]*>([^<]*):(\d+)</a>')
VSCODE_LINK = re.compile(r'href="vscode://file/([^"]*):(\d+)"')
# The source docs pages of light_controller, relative to a report directory.
LIGHT_CONTROLLER_PAGES = Path(".yanga/build/variants", VARIANT_NAME, "gtest/light_controller")
# The build picks the resolver profile with CheckCIContext; detect CI the same way.
IS_CI = any(detector.detect() for system in CISystem if (detector := system.get_detector()))
# The variant report's link to the variant test coverage page, as sphinx renders the toctree entry.
VARIANT_TEST_COVERAGE_LINK = re.compile(r'<a\b[^>]*\bhref="variant_test_coverage/index\.html"[^>]*>Variant Test Coverage</a>')
# The tokens that give a sphinx page its section nesting: a section opens, a section closes, a heading names it.
SECTION_TOKEN = re.compile(r"<section\b[^>]*>|</section>|<h[1-6]\b[^>]*>([^<]*)")
TAG = re.compile(r"<[^>]+>")


@pytest.fixture(scope="module")
def variant() -> Variant:
    """
    Build the variant as a shared library and bind to it.

    Requesting this fixture is what orders the build before the test that drives the
    library; declaration order in the file would not survive `-k` or a single node id.
    """
    config = RunCommandConfig(
        project_dir=Path.cwd(),
        platform="pc_gui",
        variant_name=VARIANT_NAME,
        not_interactive=True,
        target="build",
    )
    assert RunCommand().do_run(config) == 0, "Building the shared library failed"

    return Variant(find_library(build_dir(Path.cwd(), VARIANT_NAME), VARIANT_NAME))


@pytest.fixture(scope="module")
def gtest_build_dir() -> Path:
    """Build the variant report and the light_controller component report on gtest."""
    for target in ("report", "light_controller_report"):
        config = RunCommandConfig(
            project_dir=Path.cwd(),
            platform="gtest",
            variant_name=VARIANT_NAME,
            not_interactive=True,
            target=target,
        )
        assert RunCommand().do_run(config) == 0, f"Building {target} failed"

    return Path.cwd() / ".yanga/build/variants" / VARIANT_NAME / "gtest"


@pytest.fixture(scope="module")
def zephyr_build_dir() -> Path:
    """Build the variant report on zephyr_esp32h2."""
    config = RunCommandConfig(
        project_dir=Path.cwd(),
        platform="zephyr_esp32h2",
        variant_name=VARIANT_NAME,
        not_interactive=True,
        target="report",
    )
    assert RunCommand().do_run(config) == 0, "Building report failed"

    return Path.cwd() / ".yanga/build/variants" / VARIANT_NAME / "zephyr_esp32h2"


class Test_Disco:
    variant_name = VARIANT_NAME

    @pytest.mark.parametrize(
        ("platform", "target"),
        [
            ("pc_terminal", "report"),
            ("pc_gui", "report"),
            ("gtest", "report"),
            # The riscv64 toolchain comes from poks on every OS; native_sim needs a Linux host.
            pytest.param("zephyr_sim", "all", marks=pytest.mark.skipif(sys.platform != "linux", reason="native_sim is Linux-only")),
            ("zephyr_esp32h2", "all"),
            # A board defined in this repository (platforms/zephyr/boards), not in Zephyr.
            ("zephyr_esp32h2_waveshare", "all"),
        ],
    )
    def test_build(self, platform: str, target: str):
        # Arrange
        config = RunCommandConfig(
            project_dir=Path.cwd(),
            platform=platform,
            variant_name=self.variant_name,
            not_interactive=True,
            target=target,
        )

        # Act
        result = RunCommand().do_run(config)

        # Assert
        assert result == 0, "Building variant failed"

    def test_holding_the_power_button_turns_the_light_green(self, variant: Variant):
        """Drives the built library the way the GUI does: button in, LED colour out."""
        # Arrange
        variant.set_button(POWER_BUTTON_KEY, True)

        # Act
        for _ in range(PRESS_DEBOUNCE_STEPS - 1):
            variant.step()

        # Assert
        assert variant.led_colour() == LIGHT_OFF, "The light must stay off until the press is debounced"
        variant.step()
        assert variant.led_colour() == LIGHT_GREEN

    @pytest.mark.parametrize("report", ["reports", "light_controller/reports"])
    def test_gtest_source_docs_link_to_coverage_lines(self, gtest_build_dir: Path, report: str):
        # Arrange
        page = gtest_build_dir / report / LIGHT_CONTROLLER_PAGES / "light_controller.c.html"

        # Act
        html = page.read_text(encoding="utf-8")
        links = COVERAGE_LINK.findall(html)

        # Assert
        assert links, f"No declaration links to its coverage page in {page}"
        source_lines = (Path.cwd() / links[0][2]).read_text(encoding="utf-8").splitlines()
        for href, fragment_line, text_path, text_line in links:
            assert fragment_line == text_line, f"{href}#l{fragment_line} does not point to line {text_line}"
            assert text_path.endswith("light_controller.c")
            assert 1 <= int(fragment_line) <= len(source_lines), f"{href}#l{fragment_line} is outside {text_path}"
            assert (page.parent / href).is_file(), f"{href} does not exist"
        declaration_line = next(i for i, line in enumerate(source_lines, 1) if "void lightController(void)" in line)
        assert str(declaration_line) in {fragment_line for _, fragment_line, _, _ in links}, f"lightController does not link to #l{declaration_line}"
        assert 'href="source:' not in html, "An unresolved source: link is left"
        assert 'href="vscode://' not in html, "A production declaration fell back to VS Code"

    def test_gtest_variant_test_runs_and_reports_its_coverage(self, gtest_build_dir: Path):
        # Arrange
        junit = gtest_build_dir / "variant_test/variant_test_junit.xml"
        coverage_page = gtest_build_dir / "reports/variant_test_coverage/index.html"

        # Act
        suites = ElementTree.parse(junit).getroot()
        report = (gtest_build_dir / "reports/index.html").read_text(encoding="utf-8")

        # Assert
        assert int(suites.get("tests", 0)) > 0, f"No variant test ran in {junit}"
        assert suites.get("failures") == "0" and suites.get("errors") == "0", f"The variant test failed, see {junit}"
        # gcovr's nested report gives each covered file its own page next to the index.
        assert any(coverage_page.parent.glob("index.spled.c.*.html")), f"spled.c is missing from {coverage_page.parent}"
        assert VARIANT_TEST_COVERAGE_LINK.search(report), "The variant report does not link to the variant test coverage"

    @pytest.mark.parametrize(
        ("build_dir_fixture", "page_name", "source"),
        [
            ("gtest_build_dir", "test_light_controller.cc.html", "components/light_controller/test/test_light_controller.cc"),
            ("zephyr_build_dir", "light_controller.c.html", "components/light_controller/src/light_controller.c"),
        ],
    )
    def test_source_docs_link_to_vscode_locally_and_to_the_repository_on_ci(
        self, request: pytest.FixtureRequest, repository_url: str, head_commit: str, build_dir_fixture: str, page_name: str, source: str
    ):
        # Arrange
        build_dir = request.getfixturevalue(build_dir_fixture)
        page = build_dir / "reports" / build_dir.relative_to(Path.cwd()) / "light_controller" / page_name
        source_line_count = len((Path.cwd() / source).read_text(encoding="utf-8").splitlines())

        # Act
        html = page.read_text(encoding="utf-8")

        # Assert
        assert 'href="source:' not in html, "An unresolved source: link is left"
        if IS_CI:
            assert 'href="vscode://' not in html, "A source links to VS Code on CI"
            lines = re.findall(rf'href="{re.escape(repository_url)}/blob/{head_commit}/{re.escape(source)}#L(\d+)"', html)
            assert lines, f"No declaration links to {source} in the repository at {head_commit} in {page}"
            assert all(1 <= int(line) <= source_line_count for line in lines), f"A link points outside {source}"
            return
        assert any(
            Path(path).is_absolute() and Path(path).resolve() == (Path.cwd() / source).resolve() and 1 <= int(line) <= source_line_count
            for path, line in VSCODE_LINK.findall(html)
        ), f"No declaration links to VS Code at a line of {source} in {page}"

    def test_gtest_components_page_shows_a_folder_tree_and_the_containers_apart(self, gtest_build_dir: Path):
        # Arrange
        page = gtest_build_dir / "reports/doc/components.html"
        html = page.read_text(encoding="utf-8")

        # Act
        # Every section as (its heading and the headings it is nested in, its text).
        found, stack = [], []
        for token in SECTION_TOKEN.finditer(html):
            if token.group(0).startswith("<section"):
                stack.append(["", token.start()])
            elif token.group(0) == "</section>":
                path_titles, start = tuple(title for title, _ in stack), stack.pop()[1]
                found.append((path_titles, TAG.sub(" ", html[start : token.end()])))
            elif stack and not stack[-1][0]:
                stack[-1][0] = token.group(1).strip()
        containers = [text for titles, text in found if titles[-1] == "Containers"]
        tree = [titles for titles, _ in found if "Containers" not in titles]

        # Assert
        for component in ("rte", "spled", "light_controller", "power_button"):
            assert any(titles[-2:] == ("components", component) for titles in tree), f"{component} is not in the components folder"
        assert not any(titles[-1] == "light_application" for titles in tree), "The container light_application is a chapter of the tree"
        assert containers, f"No Containers section in {page}"
        for name in ("light_application", "power_signal_processing", "light_controller", "power_button", "main_control_knob"):
            assert re.search(rf"\b{name}\b", containers[0]), f"{name} is missing from the Containers section"

    def test_gtest_test_results_do_not_show_links_outgoing(self, gtest_build_dir: Path):
        # Arrange
        pages = list((gtest_build_dir / "reports").rglob("*_test_report.html"))

        # Act
        texts = {page: page.read_text(encoding="utf-8") for page in pages}
        showing = [page for page, text in texts.items() if "links outgoing" in text]
        unlinked = [page for page, text in texts.items() if "is part of" not in text]

        # Assert
        assert pages, "No test result page found"
        assert showing == []
        assert unlinked == [], "These test result pages do not link their suite"

    def test_gtest_report_has_no_ci_pipeline_page(self, gtest_build_dir: Path):
        # Arrange
        reports = gtest_build_dir / "reports"

        # Act
        index = (reports / "index.html").read_text(encoding="utf-8")

        # Assert
        assert not (reports / "ci_pipeline.html").exists()
        assert "ci_pipeline.html" not in index

    def test_gtest_macos_troubleshooting_is_a_how_to_not_a_platform(self, gtest_build_dir: Path):
        # Arrange
        doc = gtest_build_dir / "reports/doc"

        # Act
        platforms = (doc / "platforms/index.html").read_text(encoding="utf-8")

        # Assert
        assert "tapi error" not in platforms, "The macOS troubleshooting is still on the Platforms page"
        assert (doc / "how-to/fix-the-macos-tapi-error.html").is_file()
