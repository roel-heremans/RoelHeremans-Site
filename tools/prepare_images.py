"""Build every image the site uses into assets/img/ from the originals in this repo.

Usage:  .venv/bin/python tools/prepare_images.py [target.jpg ...]
        (no arguments: build everything; with names: rebuild only those photos)

Sources (read-only, never written): original/images/, committed.

Uses ImageMagick `convert` via subprocess (argument lists, no shell). Every
output path passes through safe_output(), which refuses anything outside
assets/img/. JPEGs are stripped of metadata; PNGs carry no date/time chunks.

og.jpg and favicon.png are drawn with TTF fonts. ImageMagick cannot read the
site's self-hosted .woff2 files, so it uses EB Garamond (a close match for
Cormorant Garamond) and Liberation Sans / DejaVu Sans (for Inter) when
installed, and falls back to ImageMagick's default font otherwise.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = (ROOT / "assets" / "img").resolve()

QUALITY = 82
HERO = 2000  # max long edge for the hero photo
STD = 1200  # max long edge for everything else
PNG_DETERMINISTIC = ["-define", "png:exclude-chunks=date,time", "+set", "date:create", "+set", "date:modify"]

# (source relative to original/, target name in assets/img/, max long edge,
#  optional crop "WxH+X+Y" in source pixels after auto-orient, optional gravity)
PHOTOS = [
    # Hero: the whole 3:2 frame; the CSS positions it (object-position 38% 30%).
    ("images/roel-portrait-door.jpg", "roel-portrait-hero.jpg", HERO, None, None),
    # Square: face centre is at x~1860 of 4898, so a 3266 square starting at x=227 centres it.
    ("images/roel-portrait-door.jpg", "roel-portrait-square.jpg", STD, "3266x3266+227+0", None),
    # Family: whole frame, everyone's face is well inside it.
    ("images/roel-family.jpg", "roel-family.jpg", STD, None, None),
]

# Open Graph portrait: 2900x3266 slice around the face, shown 560x630 on the right.
OG_SRC = "images/roel-portrait-door.jpg"
OG_CROP = "2900x3266+410+0"
OG_PHOTO_W = 560

BRAND = ("#14263A", "#1B3247", "#2B4A66")
GOLD = "#C9A24A"
SERIF_CANDIDATES = [
    "/usr/share/fonts/truetype/ebgaramond/EBGaramond12-Bold.ttf",
    "/usr/share/fonts/truetype/ebgaramond/EBGaramond12-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
]
SANS_CANDIDATES = [
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def _font(candidates: list[str]) -> list:
    for c in candidates:
        if Path(c).is_file():
            return ["-font", c]
    return []


# --- Helpers -------------------------------------------------------------------
def safe_output(path: Path) -> Path:
    """Return the resolved path if it lies inside assets/img/, else raise."""
    resolved = Path(path).resolve()
    if resolved != OUT and OUT not in resolved.parents:
        raise ValueError(f"refusing to write outside {OUT}: {resolved}")
    return resolved


def _convert(args: list, out: Path, fmt: str = "") -> Path:
    out = safe_output(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["convert", *[str(a) for a in args], f"{fmt}{out}"], check=True)
    return out


def _src(rel: str) -> str:
    path = ROOT / "original" / rel
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"{path}[0]"


JPEG_OUT = ["-strip", "-sampling-factor", "4:2:0", "-interlace", "JPEG", "-colorspace", "sRGB", "-quality", QUALITY]
FLATTEN = ["-background", "white", "-alpha", "remove", "-alpha", "off"]


# --- Builders ------------------------------------------------------------------
def build_photo(src: str, target: str, max_edge: int, crop: str | None, gravity: str | None) -> Path:
    ops = ["-auto-orient", *FLATTEN]
    if crop:
        ops += ["-gravity", gravity or "NorthWest", "-crop", crop, "+repage", "-gravity", "NorthWest"]
    ops += ["-resize", f"{max_edge}x{max_edge}>"]
    return _convert([_src(src), *ops, *JPEG_OUT], OUT / target)


def build_og() -> Path:
    """1200x630: brand gradient, portrait fading in on the right, name and tagline on the left."""
    photo_x = 1200 - OG_PHOTO_W
    # Left-to-right gradient: build a 630x1200 vertical one and rotate it.
    gradient = ["(", "-size", "630x1200", f"gradient:{BRAND[0]}-{BRAND[2]}", "-rotate", "90", ")"]
    fade_w = int(OG_PHOTO_W * .4)
    # Background colour of the gradient at the photo's left edge (x=640 of 1200).
    edge = "#203951"
    photo = ["(", _src(OG_SRC), "-auto-orient", *FLATTEN, "-crop", OG_CROP, "+repage",
             "-resize", f"{OG_PHOTO_W}x630!",
             # Fade the photo's left 40% into the background: opaque edge colour -> transparent.
             "(", "-size", f"630x{fade_w}", f"gradient:{edge}-none", "-rotate", "-90", ")",
             "-gravity", "NorthWest", "-composite", ")"]
    serif, sans = _font(SERIF_CANDIDATES), _font(SANS_CANDIDATES)
    text = [
        "-gravity", "NorthWest",
        "-fill", GOLD, "-draw", "rectangle 70,200 150,204",
        *serif, "-fill", "white", "-pointsize", 84, "-annotate", "+66+225", "Roel Heremans",
        *sans, "-fill", "#D5DEE8", "-pointsize", 30, "-annotate", "+70+345", "AI-accelerated,",
        "-annotate", "+70+385", "human-verified analytics",
        "-fill", GOLD, "-draw", "rectangle 70,450 150,452",
    ]
    return _convert([*gradient, *photo, "-gravity", "NorthWest", "-geometry", f"+{photo_x}+0",
                     "-composite", *text, *JPEG_OUT], OUT / "og.jpg")


def build_favicon() -> Path:
    """64x64: serif "RH" monogram in gold on the brand navy."""
    return _convert(
        ["-size", "64x64", f"xc:{BRAND[1]}", *_font(SERIF_CANDIDATES), "-fill", GOLD, "-pointsize", 40,
         "-gravity", "Center", "-annotate", "+0+1", "RH", "-strip", *PNG_DETERMINISTIC],
        OUT / "favicon.png", fmt="PNG32:",
    )


def main(argv: list[str] | None = None) -> int:
    """Build everything, or only the photos whose target names are passed."""
    only = set(argv or [])
    rows = [row for row in PHOTOS if not only or row[1] in only]
    if only and len(rows) != len(only):
        raise SystemExit(f"unknown photo target(s): {sorted(only - {r[1] for r in rows})}")
    produced = [build_photo(*row) for row in rows]
    if not only:
        produced += [build_og(), build_favicon()]
    for p in produced:
        print(f"{p.relative_to(ROOT)}  {p.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
