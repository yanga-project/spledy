import os
from pathlib import Path

import pytest

from yanga_core.steps.write_publish_manifest import get_commit, get_repository_url

# VS Code starts pytest in `k:\spledy`, but CMake writes the drive as `K:`, and ninja treats the two as different files.
os.chdir(Path.cwd().resolve())


@pytest.fixture(scope="session")
def repository_url() -> str:
    """The repository the reports link to, detected the way the report does."""
    url = get_repository_url(Path.cwd())
    assert url, "No repository detected from the origin remote"
    return url


@pytest.fixture(scope="session")
def head_commit() -> str:
    commit = get_commit(Path.cwd())
    assert commit, "No commit detected"
    return commit
