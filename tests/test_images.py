"""Checks on the generated image set in assets/img (made by tools/prepare_images.py):
sizes, og/favicon wiring, every image used, every referenced image present."""
import re
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import prepare_images  # noqa: E402

FIXED = ["og.jpg", "favicon.png"]


def _png_size(path):
    head = path.read_bytes()[:26]
    assert head[:8] == b"\x89PNG\r\n\x1a\n", path
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def _jpeg_size(path):
    data = path.read_bytes()
    assert data[:2] == b"\xff\xd8", path
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        (seglen,) = struct.unpack(">H", data[i + 2 : i + 4])
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack(">HH", data[i + 5 : i + 9])
            return w, h
        i += 2 + seglen
    raise AssertionError(f"no SOF marker in {path}")


@pytest.mark.parametrize("name", FIXED)
def test_og_and_favicon_exist(name):
    assert (IMG / name).is_file(), name


def test_og_is_1200x630():
    assert _jpeg_size(IMG / "og.jpg") == (1200, 630)


def test_favicon_is_64px():
    assert _png_size(IMG / "favicon.png") == (64, 64)


def test_photos_match_assets_img():
    targets = sorted(row[1] for row in prepare_images.PHOTOS)
    on_disk = sorted(p.name for p in IMG.glob("*.jpg") if p.name != "og.jpg")
    assert targets == on_disk
    assert sorted(p.name for p in IMG.iterdir() if p.suffix != ".jpg") == ["favicon.png"]


@pytest.mark.parametrize("row", prepare_images.PHOTOS, ids=lambda r: r[1])
def test_photo_size_limits(row):
    target, max_edge = row[1], row[2]
    w, h = _jpeg_size(IMG / target)
    assert max(w, h) <= max_edge, (target, w, h)
    assert (IMG / target).stat().st_size < 500 * 1024, target


def test_content_dimensions_match_files():
    from content import CONTENT  # noqa: PLC0415
    for key, im in CONTENT["images"].items():
        assert _jpeg_size(ROOT / im["src"]) == (im["w"], im["h"]), key


def test_output_guard_refuses_paths_outside_assets_img(tmp_path):
    with pytest.raises(ValueError):
        prepare_images.safe_output(tmp_path / "x.jpg")
    with pytest.raises(ValueError):
        prepare_images.safe_output(IMG / ".." / "evil.jpg")
    assert prepare_images.safe_output(IMG / "ok.jpg") == (IMG / "ok.jpg").resolve()


def test_og_and_favicon_are_wired_unconditionally(built):
    pages = [p for p in built.rglob("index.html") if "og:title" in p.read_text(encoding="utf-8")]
    assert len(pages) >= 5
    for page in pages:
        html = page.read_text(encoding="utf-8")
        assert 'assets/img/favicon.png"' in html, page
        assert re.search(r'<meta property="og:image" content="https?://[^"]+/assets/img/og\.jpg">', html), page


def test_every_image_is_used(built):
    texts = [p.read_text(encoding="utf-8") for p in built.rglob("*")
             if p.is_file() and p.suffix in {".html", ".css"}]
    unused = [f.name for f in sorted(IMG.iterdir())
              if f.is_file() and not any(f"img/{f.name}" in t for t in texts)]
    assert not unused, unused


def test_every_referenced_image_exists(built):
    refs = set()
    for p in built.rglob("*"):
        if p.is_file() and p.suffix in {".html", ".css"}:
            refs |= set(re.findall(r"assets/img/([\w.\-]+)", p.read_text(encoding="utf-8")))
    assert refs
    missing = sorted(r for r in refs if not (IMG / r).is_file())
    assert not missing, missing
