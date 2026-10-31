"""Page content: every page carries its copy, anchors resolve, CV, Bitcoin, copy button, hero."""
import re
from html.parser import HTMLParser
from pathlib import Path

from content import CONTENT
from paths import page_path

ROOT = Path(__file__).resolve().parent.parent
PAGES = {p["id"]: p for p in CONTENT["pages"]}
CSS = (ROOT / "assets" / "css" / "styles.css").read_text()
JS = (ROOT / "assets" / "js" / "site.js").read_text()


def html_of(built, page_id):
    return (built / page_path(PAGES[page_id]) / "index.html").read_text()


def main_of(html):
    return html.split('<main id="main">', 1)[1].split("</main>", 1)[0]


def text(html):
    """Visible text, tags removed, entities for quotes decoded, whitespace collapsed."""
    t = re.sub(r"<[^>]+>", " ", html)
    t = t.replace("&ldquo;", "“").replace("&rdquo;", "”").replace("&amp;", "&")
    t = t.replace("&#34;", '"').replace("&#39;", "'").replace("&quot;", '"')
    return re.sub(r"\s+", " ", t).strip()


def headings(html, level):
    return [text(h) for h in re.findall(rf"<h{level}[^>]*>(.*?)</h{level}>", html, re.S)]


def ids(html):
    return set(re.findall(r'\bid="([^"]+)"', html))


# Key section headings per page (h2) and items (h3), in order.
H2 = {
    "home": ["AI does the heavy lifting. I do the checking.", "What “hand-tested” means",
             "Recent projects", "I prefer to be paid in Bitcoin", "Bring me your analytics question"],
    "approach": ["Four steps", "What “hand-tested” means", "What changes for you",
                 "Typical engagements", "Bring me your analytics question"],
    "work": ["Best Way Healthcare", "Impala Studios: severe-weather triggers with GraphCast",
             "Earlier projects", "Bring me your analytics question"],
    "about": ["Where I have worked", "Certificates", "Family, yoga and kombucha",
              "Bring me your analytics question"],
    "contact": ["I prefer to be paid in Bitcoin"],
}


def test_every_page_renders_its_key_headings(built):
    for page_id, want in H2.items():
        assert headings(main_of(html_of(built, page_id)), 2) == want, page_id
    assert headings(html_of(built, "approach"), 3) == \
        ["Scope", "Build", "Verify", "Deliver"] + [s["name"] for s in CONTENT["approach"]["services"]["items"]]
    assert headings(html_of(built, "work"), 3) == \
        [p["name"] for p in CONTENT["work"]["earlier"]["items"]]
    assert headings(html_of(built, "about"), 3) == \
        [t["role"] for t in CONTENT["about"]["timeline"]["items"]]


def test_redirect_anchors_exist_on_target_page(built):
    """Every old /project/* URL lands on an element that exists."""
    anchored = {old: t for old, t in CONTENT["redirects"].items() if "anchor" in t}
    assert len(anchored) == 6
    for old, target in anchored.items():
        assert target["anchor"] in ids(html_of(built, target["page"])), old
    work = html_of(built, "work")
    for anchor in ("bef4u", "electrolux", "uptime", "political-monitor", "fbeta", "sniffers"):
        assert re.search(rf'<article class="card project" id="{anchor}"', work), anchor


def test_in_page_anchor_links_resolve(built):
    """Every internal link with a #fragment points at an id on its target page."""
    root = built.resolve()
    checked = 0
    for page in CONTENT["pages"]:
        f = built / page_path(page) / "index.html"
        for href in re.findall(r'href="([^"]+#[^"]+)"', f.read_text()):
            if href.startswith(("http", "mailto:")):
                continue
            path, _, frag = href.partition("#")
            target = (f.parent / path).resolve() if path else f.resolve()
            target = target / "index.html" if target.is_dir() else target
            assert root in target.parents, href
            assert frag in ids(target.read_text()), (page["id"], href)
            checked += 1
    assert checked >= 3  # home -> work#best-way-healthcare, work#impala-studios, contact#bitcoin


def test_home_hero_strike_and_log(built):
    html = html_of(built, "home")
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S).group(1)
    assert re.search(r'<s class="fix__old">months<svg class="fix__strike"[^>]*aria-hidden="true"', h1)
    assert '<em class="fix__new">days</em>' in h1
    # The draw-in only runs with motion allowed; otherwise the line is there from the start.
    motion = re.search(r"@media \(prefers-reduced-motion: no-preference\) \{\s*\.fix__strike path \{[^}]*animation: strike-draw", CSS)
    assert motion, "strike animation must sit inside the no-preference media query"
    assert CSS.count("animation: strike-draw") == 1
    base = re.search(r"\n\.fix__strike path \{([^}]*)\}", CSS).group(1)
    assert "dash" not in base, "outside the motion query the line must be fully drawn"
    # Verification log: marked "example", system mono stack, the six steps.
    log = re.search(r'<figure class="vlog".*?</figure>', html, re.S).group(0)
    assert '<span class="vlog__marker">example</span>' in log
    assert len(re.findall(r'class="vlog__tag vlog__tag--(claude|roel|flag)"', log)) == 6
    assert "verified, ready for the client" in log
    assert re.search(r"\.vlog \{[^}]*font-family: var\(--mono\)", CSS)
    assert re.search(r"--mono: ui-monospace,[^;]*monospace;", CSS)
    for fact in ("20+ years", "50+ projects", "PhD"):
        assert f"<dt>{fact}</dt>" in html


def test_hand_tested_ticks_and_comparison_table(built):
    for page_id in ("home", "approach"):
        ul = re.search(r'<ul class="tick-list">(.*?)</ul>', html_of(built, page_id), re.S).group(1)
        assert len(re.findall(r"<li>", ul)) == 5, page_id
    assert re.search(r"\.tick-list li::before \{[^}]*color: var\(--ok\)", CSS)
    html = html_of(built, "approach")
    wrap = re.search(r'<div class="table-scroll"[^>]*>\s*<table class="compare">(.*?)</table>', html, re.S)
    assert wrap, "comparison table sits in its scroll wrapper"
    assert len(re.findall(r"<tr>", wrap.group(1))) == 1 + 5
    assert re.search(r"\.table-scroll \{[^}]*overflow-x: auto", CSS)


def test_impala_pipeline_row(built):
    html = html_of(built, "work")
    impala = re.search(r'id="impala-studios".*?</section>', html, re.S).group(0)
    steps = re.findall(r"<li[^>]*>([^<]+)</li>", re.search(r'<ol class="pipeline">(.*?)</ol>', impala, re.S).group(1))
    assert steps == ["ERA5 / CDS", "GraphCast", "Event detectors", "Trigger", "Alerts API + Slack"]
    assert '<li class="pipeline__trigger">Trigger</li>' in impala


def test_about_testimonial_certificates_and_outside_work(built):
    html = main_of(html_of(built, "about"))
    assert html.count("<blockquote>") == 2  # the one testimonial + the Dalai Lama quote
    assert "Christos Tsirogiannis, co-worker at Polpo" in html
    assert "“Give the ones you love, wings to fly, roots to come back and reasons to stay.”" in text(html)
    assert "Dalai Lama" in html
    for cert in CONTENT["about"]["certificates"]["items"]:
        assert cert in text(html)
    assert 'src="../assets/img/roel-family.jpg"' in html
    assert 'src="../assets/img/roel-portrait-square.jpg"' in html
    assert 'src="./assets/img/roel-portrait-hero.jpg"' in html_of(built, "home")


def test_cv_is_served_and_linked(built):
    cv = built / "cv" / "roel-heremans-cv.pdf"
    assert cv.is_file()
    assert cv.read_bytes() == (ROOT / "original" / "roel-heremans-cv.pdf").read_bytes()
    assert 'href="../cv/roel-heremans-cv.pdf"' in html_of(built, "contact")
    assert 'href="../cv/roel-heremans-cv.pdf"' in html_of(built, "about")
    assert "framerusercontent" not in "".join(html_of(built, p) for p in PAGES)


def test_contact_email_copy_button_is_progressive(built):
    html = html_of(built, "contact")
    email = CONTENT["links"]["email"]
    # Visible, selectable text plus a mailto link, without JS.
    assert f'<code class="copyline__email" id="contact-email">{email}</code>' in html
    assert f'href="mailto:{email}?subject=Analytics%20project"' in html
    # The button starts hidden and site.js reveals it and wires it to the clipboard.
    btn = re.search(r'<button class="copy-btn"[^>]*>([^<]+)</button>', html)
    assert btn and btn.group(1) == "Copy" and 'data-copy="contact-email"' in btn.group(0)
    assert " hidden>" in btn.group(0)
    assert "btn.hidden = false" in JS and "navigator.clipboard.writeText" in JS
    assert re.search(r"\.copy-btn\[hidden\] \{ display: none; \}", CSS)
    assert 'href="https://www.linkedin.com/in/roel-heremans/"' in main_of(html)


def test_bitcoin_section(built):
    html = html_of(built, "contact")
    sec = re.search(r'<section class="btc-card" id="bitcoin".*?</section>', html, re.S)
    assert sec, "Bitcoin section with id=bitcoin on Contact"
    t = text(sec.group(0))
    assert "₿" in sec.group(0)
    assert "I prefer to be paid in Bitcoin" in t
    for phrase in ("Quotes and invoices are in euros", "exchange rate on the invoice date",
                   "On-chain or Lightning", "fresh payment address comes with each invoice",
                   "Bank transfer in EUR"):
        assert phrase in t, phrase
    # Home: the short note links to the full section.
    home = html_of(built, "home")
    assert "I prefer to be paid in Bitcoin" in home
    assert 'href="contact/#bitcoin"' in home
    # No Bitcoin address is published anywhere (legacy, P2SH, bech32, Lightning invoice).
    addr = re.compile(r"\b(?:bc1[02-9ac-hj-np-z]{11,71}|[13][1-9A-HJ-NP-Za-km-z]{25,34}|lnbc[0-9a-z]{20,})\b")
    for f in built.rglob("*.html"):
        assert not addr.search(f.read_text()), f


class _DraftText(HTMLParser):
    """Text of the draft's content elements (main only), one string per element."""
    TAGS = {"p", "li", "h1", "h2", "h3", "h4", "td", "th", "dt", "dd", "strong"}

    def __init__(self):
        super().__init__()
        self.in_main, self.stack, self.out = False, [], []

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.in_main = True
        if self.in_main and tag in self.TAGS:
            self.stack.append([tag, ""])

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False
        if self.stack and self.stack[-1][0] == tag:
            _, t = self.stack.pop()
            t = re.sub(r"\s+", " ", t).strip()
            if t:
                self.out.append(t)

    def handle_data(self, data):
        for item in self.stack:
            item[1] += " " + data


# Draft texts deliberately changed when moving into the site (with the reason).
DRAFT_EXCEPTIONS = {
    # h1: "months" is struck through (<s>), so it reads differently; checked in test_build
    # and test_home_hero_strike_and_log.
    "Your analytics question, answered in months days . Every number checked by hand.",
}


def _norm(t):
    """Compare words only: curly quotes straightened, arrows (drawn by CSS on the pipeline)
    and a./b./c. list markers (drawn by CSS on Contact) dropped."""
    t = t.replace("\u201c", '"').replace("\u201d", '"').replace("\u2192", " ")
    t = re.sub(r"^[a-c]\. ", "", t)
    return re.sub(r"\s+", " ", t).strip()


def test_all_draft_copy_is_on_the_site(built):
    parser = _DraftText()
    parser.feed((ROOT / "original" / "draft" / "roel-heremans.html").read_text())
    site = _norm(" ".join(text(main_of(html_of(built, p))) for p in PAGES))
    missing = []
    for t in parser.out:
        if t in DRAFT_EXCEPTIONS:
            continue
        if t.startswith("Certificates:"):
            # The inline list became a heading plus one item per certificate.
            parts = t.split(":", 1)[1].rstrip(".").split("), ")
            assert all(_norm(p) in site for p in parts), t
            continue
        if _norm(t) not in site:
            missing.append(t)
    assert len(parser.out) > 60
    assert not missing, missing
