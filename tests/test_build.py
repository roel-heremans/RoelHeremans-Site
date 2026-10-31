import re

from build import content_for_env
from content import CONTENT
from paths import page_path, rel

PATHS = ["", "approach/", "work/", "about/", "contact/"]
PAGES = {p["id"]: p for p in CONTENT["pages"]}
NOINDEX = '<meta name="robots" content="noindex">'
BASE = "https://www.roel-heremans.com/"


def h1_text(html):
    """Plain text of the <h1>, without struck-through (<s>) words and without tags."""
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S).group(1)
    h1 = re.sub(r"<s\b.*?</s>", "", h1, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h1)).strip()


def page_files(root):
    return [root / page_path(p) / "index.html" for p in CONTENT["pages"]]


def _resolve(page_file, href):
    target = (page_file.parent / href.split("#", 1)[0]).resolve()
    return target / "index.html" if target.is_dir() else target


def test_five_pages(built):
    for p in PATHS:
        assert (built / p / "index.html").is_file(), p
    assert sorted(page_files(built)) == sorted(built / p / "index.html" for p in PATHS)


def test_rel_keeps_anchor_and_trailing_slash():
    assert rel("", "work/") == "work/"
    assert rel("work/", "") == "../"
    assert rel("project/uptime/", "work/#uptime") == "../../work/#uptime"
    assert rel("about/", "about/") == "./"


def test_html_lang_and_single_h1(built):
    for page in CONTENT["pages"]:
        html = (built / page_path(page) / "index.html").read_text()
        assert '<html lang="en">' in html
        assert html.count("<h1") == 1, page["id"]
        assert h1_text(html) == page["heading"], page["id"]


def test_title_and_head_meta(built):
    for page in CONTENT["pages"]:
        path = page_path(page)
        html = (built / path / "index.html").read_text()
        title = page.get("full_title") or f"{page['title']} | Roel Heremans"
        assert f"<title>{title}</title>" in html, page["id"]
        d = re.search(r'<meta name="description" content="([^"]+)"', html)
        assert d and d.group(1).strip(), path
        assert f'<meta property="og:url" content="{BASE}{path}">' in html
        for prop in ("og:title", "og:description", "og:locale", "og:site_name"):
            assert re.search(rf'<meta property="{prop}" content="[^"]+">', html), (path, prop)
        assert "assets/css/styles.css" in html and "assets/js/site.js" in html
        assert "hreflang" not in html and "lang-switch" not in html


def test_home_title_is_the_pitch(built):
    assert "<title>Roel Heremans · AI-accelerated, human-verified analytics</title>" in \
        (built / "index.html").read_text()


def test_header_nav_cta_and_footer(built):
    nav_ids = ["approach", "work", "about", "contact"]
    assert [p["id"] for p in CONTENT["pages"] if p["in_nav"]] == nav_ids
    root = built.resolve()
    for page in CONTENT["pages"]:
        f = built / page_path(page) / "index.html"
        html = f.read_text()
        nav = re.search(r'<nav class="site-nav".*?</nav>', html, re.S).group(0)
        assert re.findall(r"<a [^>]*>([^<]+)</a>", nav) == ["Approach", "Work", "About", "Contact"]
        hrefs = re.findall(r'href="([^"]+)"', nav)
        assert [_resolve(f, h) for h in hrefs] == \
            [root / page_path(PAGES[i]) / "index.html" for i in nav_ids], f
        assert nav.count('aria-current="page"') == (1 if page["in_nav"] else 0), f
        cta = re.search(r'<a class="btn btn--accent nav-cta" href="([^"]+)">Start a project</a>', html)
        assert cta and _resolve(f, cta.group(1)) == root / "contact" / "index.html", f
        assert 'class="menu-toggle"' in html and 'aria-controls="site-nav"' in html
        assert re.search(r'<a class="wordmark" href="[^"]+">Roel Heremans</a>', html)
        assert 'href="https://www.linkedin.com/in/roel-heremans/"' in html
        assert 'href="mailto:roel.heremans@gmail.com"' in html
        assert re.search(r"© 20\d\d Roel Heremans", html)
        assert "<img" not in html.split("<main", 1)[0], "header is real text, no logo image"


def test_preview_noindex(built):
    for f in page_files(built):
        html = f.read_text()
        assert NOINDEX in html, f
        assert 'rel="canonical"' not in html, f
    assert (built / "robots.txt").read_text() == "User-agent: *\nDisallow: /\n"


def test_production_indexable(built_production):
    assert content_for_env({"SITE_ENV": "production"})["preview"] is False
    assert CONTENT["preview"] is True  # the shared dict is not mutated
    for p, f in zip(PATHS, page_files(built_production)):
        html = f.read_text()
        assert "noindex" not in html, f
        assert f'<link rel="canonical" href="{BASE}{p}">' in html, f
    robots = (built_production / "robots.txt").read_text()
    assert "Disallow" not in robots
    assert f"Sitemap: {BASE}sitemap.xml" in robots


def test_default_env_keeps_preview():
    assert content_for_env({})["preview"] is True
    assert content_for_env({"SITE_ENV": "staging"})["preview"] is True


def test_sitemap_lists_the_five_pages(built):
    locs = re.findall(r"<loc>([^<]+)</loc>", (built / "sitemap.xml").read_text())
    assert sorted(locs) == sorted(BASE + p for p in PATHS)


# Old Framer URL -> new output path + anchor.
OLD_URLS = {
    "project/Electrolux": "work/#electrolux",
    "project/PoliticalMonitor": "work/#political-monitor",
    "project/bef4U": "work/#bef4u",
    "project/fbeta": "work/#fbeta",
    "project/sniffers": "work/#sniffers",
    "project/uptime": "work/#uptime",
    "de": "",
}


def test_old_urls_redirect(built):
    root = built.resolve()
    assert set(CONTENT["redirects"]) == set(OLD_URLS)
    for old, want in OLD_URLS.items():
        f = built / old / "index.html"
        html = f.read_text()
        m = re.search(r'<meta http-equiv="refresh" content="0; url=([^"]+)">', html)
        assert m, old
        target = m.group(1)
        want_path, _, anchor = want.partition("#")
        assert _resolve(f, target) == root / want_path / "index.html", (old, target)
        assert target.endswith(f"#{anchor}" if anchor else "/"), (old, target)
        assert f'<link rel="canonical" href="{BASE}{want}">' in html, old
        assert f'<a href="{target}">' in html.split("<body", 1)[1], old
        assert NOINDEX in html
