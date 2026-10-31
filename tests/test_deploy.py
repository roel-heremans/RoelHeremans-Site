"""Checks on the STRATO deploy: workflow shape, plan/safety logic, production output (no network)."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from deploy_strato import MANIFEST, SITE, check_remote_path, local_manifest, plan  # noqa: E402

WORKFLOW = (ROOT / ".github" / "workflows" / "deploy.yml").read_text()


def strato_job():
    return WORKFLOW.split("\n  strato:\n", 1)[1]


def test_workflow_strato_job_gated_and_after_build():
    job = strato_job()
    assert "needs: build" in job
    assert "if: vars.STRATO_DEPLOY == 'true'" in job
    assert "SITE_ENV=production ./build-output.sh" in job
    assert "python tools/deploy_strato.py output" in job
    for name in ("STRATO_HOST", "STRATO_USER", "STRATO_PASSWORD", "STRATO_PORT"):
        assert f"{name}: ${{{{ secrets.{name} }}}}" in job
    assert "STRATO_REMOTE_PATH: ${{ vars.STRATO_REMOTE_PATH }}" in job


def test_pages_deploy_not_gated_and_stays_preview():
    pages = WORKFLOW.split("\n  deploy:\n", 1)[1].split("\n  strato:\n", 1)[0]
    assert "STRATO" not in pages and "vars." not in pages
    assert "SITE_ENV" not in WORKFLOW.split("\n  strato:\n", 1)[0]


def test_paramiko_in_requirements():
    assert "paramiko" in (ROOT / "requirements.txt").read_text()


def test_manifest_is_site_specific():
    assert MANIFEST == ".roelheremans-deploy.json"
    assert SITE == "roelheremans"


def test_known_hosts_present():
    text = (ROOT / "tools" / "strato_known_hosts").read_text()
    assert "strato.hosting ssh-ed25519" in text


@pytest.mark.parametrize("path", ["", "/", "htdocs", "/htdocs", "/htdocs/", ".", "/htdocs/.."])
def test_refuses_webspace_root(path):
    with pytest.raises(SystemExit):
        check_remote_path(path)


def test_accepts_dedicated_folder():
    assert check_remote_path("/roelheremans/") == "/roelheremans"
    assert check_remote_path("/htdocs/roelheremans") == "/htdocs/roelheremans"


def test_refuses_foreign_folder():
    # A non-empty folder without our manifest belongs to something else (kombucha, sattva).
    with pytest.raises(SystemExit):
        plan({"index.html": "a"}, remote_manifest=None, remote_entries=["index.html", "img"])


def test_first_deploy_into_empty_folder_uploads_everything():
    uploads, deletes = plan({"index.html": "a", "work/index.html": "b"}, None, [])
    assert uploads == ["index.html", "work/index.html"]
    assert deletes == []


def test_only_changed_files_uploaded_and_stale_ones_deleted():
    old = {"site": SITE, "files": {"index.html": "a", "old/index.html": "x", "work/index.html": "b"}}
    uploads, deletes = plan({"index.html": "a", "work/index.html": "B"}, old, ["index.html", "old", "work", MANIFEST])
    assert uploads == ["work/index.html"]
    assert deletes == ["old/index.html"]


def test_unmanifested_remote_files_never_deleted():
    old = {"site": SITE, "files": {"index.html": "a"}}
    _, deletes = plan({"index.html": "a"}, old, ["index.html", "foreign.txt", MANIFEST])
    assert deletes == []


@pytest.mark.parametrize("other", ["realhealthkombucha", "something-else"])
def test_manifest_of_other_site_refused(other):
    with pytest.raises(SystemExit):
        plan({"index.html": "a"}, {"site": other, "files": {}}, ["index.html", MANIFEST])


def test_local_manifest_hashes_build(built):
    files = local_manifest(built)
    assert "index.html" in files and "robots.txt" in files
    assert all(len(h) == 64 for h in files.values())
    assert MANIFEST not in files


def test_htaccess_only_on_live_build(built, built_production):
    assert not (built / ".htaccess").exists()
    rules = (built_production / ".htaccess").read_text()
    assert "RewriteRule ^(.*)$ https://www.roel-heremans.com/$1 [R=301,L]" in rules
    assert "%{HTTPS} !=on" in rules
    assert "%{HTTP_HOST} !^www\\." in rules
    assert ".htaccess" in local_manifest(built_production)


def test_production_robots_allow_all_and_no_noindex(built_production):
    robots = (built_production / "robots.txt").read_text()
    assert "Disallow" not in robots
    assert "Sitemap: https://www.roel-heremans.com/sitemap.xml" in robots
    assert "noindex" not in (built_production / "index.html").read_text()


def test_preview_stays_noindex(built):
    assert (built / "robots.txt").read_text() == "User-agent: *\nDisallow: /\n"
    assert "noindex" in (built / "index.html").read_text()
