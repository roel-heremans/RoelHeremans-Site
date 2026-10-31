"""All colours live as tokens in the one :root block of styles.css (Roel's ink-blue + gold palette)."""
import re
from pathlib import Path

CSS = (Path(__file__).resolve().parent.parent / "assets" / "css" / "styles.css").read_text()
COLOUR_RE = re.compile(r"#[0-9a-fA-F]{3,8}(?![\w-])|\b(?:rgba?|hsla?)\(", re.I)
ALLOWED = {"#fff", "#ffffff"}


def _strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def _split_token_block(css):
    m = re.search(r":root\s*\{[^}]*\}", css)
    assert m, "no :root block"
    return m.group(0), css[: m.start()] + css[m.end():]


def colours_outside_tokens(css):
    _, rest = _split_token_block(_strip_comments(css))
    return [c for c in COLOUR_RE.findall(rest) if c.lower() not in ALLOWED]


def test_no_colour_outside_root_tokens():
    assert colours_outside_tokens(CSS) == []


def test_rule_catches_stray_colours():
    css = ":root { --a: #123456; }\n.x { color: #abc; }\n.y { background: rgba(0,0,0,.2); }\n.z { color: #fff; }"
    assert colours_outside_tokens(css) == ["#abc", "rgba("]


def test_one_colour_block_with_the_palette_tokens():
    tokens, rest = _split_token_block(_strip_comments(CSS))
    for name in ("--brand", "--brand-deep", "--grad-feature", "--accent", "--accent-text", "--ok",
                 "--bg", "--bg-alt", "--surface", "--line", "--text", "--muted", "--light"):
        assert re.search(rf"{name}\s*:", tokens), name
    assert re.search(r"--brand\s*:\s*#2B4A66\s*;", tokens)
    assert re.search(r"--accent\s*:\s*#C9A24A\s*;", tokens)
    # Later :root blocks (media queries) may only change sizes, never colours.
    for block in re.findall(r":root\s*\{[^}]*\}", rest):
        assert not COLOUR_RE.search(block), block


def _token(name):
    return re.search(rf"{name}\s*:\s*(#[0-9A-Fa-f]{{6}})\s*;", _strip_comments(CSS)).group(1)


def _luminance(hex_):
    c = [int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    hi, lo = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def test_small_text_contrast():
    """Small text must reach 4.5:1 on the light backgrounds (and gold on the dark brand)."""
    for fg in ("--text", "--muted", "--accent-text", "--ok", "--brand"):
        for bg in ("--bg", "--bg-alt", "--surface"):
            assert contrast(_token(fg), _token(bg)) >= 4.5, (fg, bg)
    assert contrast(_token("--accent"), _token("--brand-deep")) >= 4.5


def test_every_var_is_defined():
    defined = set(re.findall(r"(--[\w-]+)\s*:", CSS))
    used = set(re.findall(r"var\((--[\w-]+)", CSS))
    assert used - defined == set()
