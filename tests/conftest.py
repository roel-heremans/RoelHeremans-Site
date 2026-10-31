import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from build import build, content_for_env  # noqa: E402
from content import CONTENT  # noqa: E402


@pytest.fixture(scope="session")
def built(tmp_path_factory):
    """The preview site (CONTENT as committed), built once per test run."""
    out = tmp_path_factory.mktemp("site") / "out"
    build(out, CONTENT)
    return out


@pytest.fixture(scope="session")
def built_production(tmp_path_factory):
    """The live site, built with the content SITE_ENV=production uses."""
    out = tmp_path_factory.mktemp("site_prod") / "out"
    build(out, content_for_env({"SITE_ENV": "production"}))
    return out
