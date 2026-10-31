"""Upload output/ to the STRATO webspace over SFTP (the live roel-heremans.com).

Usage:  SITE_ENV=production ./build-output.sh && python tools/deploy_strato.py [output]

Connection details come from the environment (GitHub secrets in CI, never the repo):
  STRATO_HOST, STRATO_USER, STRATO_PASSWORD, STRATO_PORT (default 22),
  STRATO_REMOTE_PATH  the site's own folder, e.g. /roelheremans

Safety: the webspace also hosts realhealthkombucha.com and sattva-reset.com, so the script refuses the
webspace root, and refuses a non-empty folder unless it holds our manifest
(.roelheremans-deploy.json, written after every deploy). It only uploads changed files
and only deletes files that an earlier deploy of this site put there. The
server's host key must match tools/strato_known_hosts.
"""
from __future__ import annotations

import hashlib
import json
import os
import posixpath
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOWN_HOSTS = ROOT / "tools" / "strato_known_hosts"
MANIFEST = ".roelheremans-deploy.json"
SITE = "roelheremans"
FORBIDDEN = {"", "/", ".", "htdocs", "/htdocs"}


def check_remote_path(path: str) -> str:
    norm = posixpath.normpath(path) if path else ""
    if norm in FORBIDDEN:
        sys.exit(f"Refusing to deploy into the webspace root ({path!r}); use the site's own folder.")
    return norm


def local_manifest(out_dir: Path) -> dict[str, str]:
    out_dir = Path(out_dir)
    return {
        p.relative_to(out_dir).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(out_dir.rglob("*"))
        if p.is_file() and p.name != MANIFEST
    }


def plan(local: dict[str, str], remote_manifest: dict | None,
         remote_entries: list[str]) -> tuple[list[str], list[str]]:
    if remote_manifest is None:
        if remote_entries:
            sys.exit("Remote folder is not empty and has no deploy manifest: it is not this site's folder.")
        old = {}
    else:
        if remote_manifest.get("site") != SITE:
            sys.exit(f"Remote manifest belongs to {remote_manifest.get('site')!r}, not {SITE!r}.")
        old = remote_manifest.get("files", {})
    uploads = sorted(f for f, h in local.items() if old.get(f) != h)
    deletes = sorted(f for f in old if f not in local)
    return uploads, deletes


def _mkdirs(sftp, path: str) -> None:
    parts = path.strip("/").split("/")
    cur = "/" if path.startswith("/") else ""
    for part in parts:
        cur = posixpath.join(cur, part) if cur else part
        try:
            sftp.stat(cur)
        except OSError:
            sftp.mkdir(cur)
            sftp.chmod(cur, 0o755)


def deploy(out_dir: Path) -> None:
    import paramiko

    env = os.environ
    missing = [k for k in ("STRATO_HOST", "STRATO_USER", "STRATO_PASSWORD", "STRATO_REMOTE_PATH") if not env.get(k)]
    if missing:
        sys.exit("Missing environment: " + ", ".join(missing))
    remote = check_remote_path(env["STRATO_REMOTE_PATH"])
    local = local_manifest(out_dir)
    if "index.html" not in local:
        sys.exit(f"No index.html in {out_dir}; build first.")

    client = paramiko.SSHClient()
    client.load_host_keys(str(KNOWN_HOSTS))
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.connect(env["STRATO_HOST"].strip(), port=int(env.get("STRATO_PORT") or "22"),
                   username=env["STRATO_USER"].strip(), password=env["STRATO_PASSWORD"].rstrip("\r\n"),
                   look_for_keys=False, allow_agent=False)
    sftp = client.open_sftp()
    try:
        if not remote.startswith("/"):
            remote = posixpath.join(sftp.normalize("."), remote)
        try:
            entries = sftp.listdir(remote)
        except OSError:
            entries = []
        manifest = None
        if MANIFEST in entries:
            with sftp.open(posixpath.join(remote, MANIFEST)) as f:
                manifest = json.loads(f.read())
        uploads, deletes = plan(local, manifest, entries)
        _mkdirs(sftp, remote)
        if manifest is None:  # claim the empty folder first, so an interrupted deploy can resume
            with sftp.open(posixpath.join(remote, MANIFEST), "w") as f:
                f.write(json.dumps({"site": SITE, "files": {}}))
        for rel in uploads:
            target = posixpath.join(remote, rel)
            _mkdirs(sftp, posixpath.dirname(target))
            sftp.put(str(Path(out_dir) / rel), target)
            sftp.chmod(target, 0o644)
            print(f"  up  {rel}")
        for rel in deletes:
            try:
                sftp.remove(posixpath.join(remote, rel))
                print(f"  del {rel}")
            except OSError:
                pass
        with sftp.open(posixpath.join(remote, MANIFEST), "w") as f:
            f.write(json.dumps({"site": SITE, "files": local}, indent=0))
        print(f"Done: {len(uploads)} uploaded, {len(deletes)} deleted, {len(local)} files in {remote}")
    finally:
        sftp.close()
        client.close()


if __name__ == "__main__":
    deploy(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "output")
