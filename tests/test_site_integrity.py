import re
from urllib.parse import unquote

SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "//", "data:", "javascript:")
ATTR_RE = re.compile(r"""\b(?:href|src)\s*=\s*(["'])(.*?)\1""", re.I | re.S)
URL_RE = re.compile(r"""url\(\s*(["']?)(.*?)\1\s*\)""", re.I | re.S)
# Photos that Task 3 (tools/prepare_images.py) creates. Until they exist, a missing file at
# exactly these paths is tolerated; once they exist they are checked like every other link.
# Task 3: remove this exemption.
PENDING_IMAGES = {"assets/img/roel-portrait-hero.jpg", "assets/img/roel-portrait-square.jpg",
                  "assets/img/roel-family.jpg"}


def _files(out, exts):
    return [p for p in sorted(out.rglob("*")) if p.is_file() and p.suffix in exts]


def _refs(path):
    text = path.read_text(encoding="utf-8")
    refs = [m.group(2) for m in ATTR_RE.finditer(text)] if path.suffix == ".html" else []
    refs += [m.group(2) for m in URL_RE.finditer(text)]
    return refs


def _resolve(base_file, ref):
    ref = ref.strip()
    if not ref or ref.startswith("#") or ref.startswith(SKIP_PREFIXES):
        return None
    ref = ref.split("#", 1)[0].split("?", 1)[0]
    if not ref:
        return None
    target = (base_file.parent / unquote(ref)).resolve()
    return target / "index.html" if target.is_dir() else target


def test_internal_links_resolve(built):
    root = built.resolve()
    missing, count = [], 0
    for p in _files(built, {".html", ".css"}):
        for ref in _refs(p):
            target = _resolve(p, ref)
            if target is None:
                continue
            count += 1
            if root in target.parents and not target.exists() and \
                    str(target.relative_to(root)) in PENDING_IMAGES:
                continue
            if not target.is_file() or root not in target.parents:
                missing.append((str(p.relative_to(built)), ref))
    assert count > 5 * 8
    assert not missing, missing


def test_no_root_absolute_urls(built):
    """The test site lives under /RoelHeremans-Site/, so every internal link is relative."""
    pat = re.compile(r"""(?:href|src)\s*=\s*["']/(?!/)|url\(\s*["']?/(?!/)""", re.I)
    bad = [str(p) for p in _files(built, {".html", ".css"}) if pat.search(p.read_text())]
    assert not bad, bad


def test_scan_covers_pages_and_redirects(built):
    assert len(_files(built, {".html"})) == 5 + 7
