"""Case-study pages: one per earlier project, generated from the same data as the /work/ cards."""
import re

from content import CONTENT
from paths import page_path

PROJECTS = CONTENT["work"]["earlier"]["items"]
PAGES = {p["id"]: p for p in CONTENT["pages"]}
PREVIEW_BASE = "https://roel-heremans.github.io/RoelHeremans-Site/"


def case_file(built, project_id):
    return built / "work" / project_id / "index.html"


def main_of(html):
    return html.split('<main id="main">', 1)[1].split("</main>", 1)[0]


def text(html):
    t = re.sub(r"<[^>]+>", " ", html)
    t = t.replace("&ldquo;", "“").replace("&rdquo;", "”").replace("&amp;", "&")
    t = t.replace("&#34;", '"').replace("&#39;", "'").replace("&quot;", '"')
    return re.sub(r"\s+", " ", t).strip()


def resolve(page_file, href):
    target = (page_file.parent / href.split("#", 1)[0]).resolve()
    return target / "index.html" if target.is_dir() else target


def test_seven_projects_spryfox_first_and_wide():
    assert [p["id"] for p in PROJECTS] == [
        "spryfox", "bef4u", "electrolux", "uptime", "political-monitor", "fbeta", "sniffers"]
    # 1 wide card + 6 = two full rows of three at desktop: no orphan card.
    wide = [p["id"] for p in PROJECTS if p.get("wide")]
    assert wide == ["spryfox"]
    assert (len(PROJECTS) - len(wide)) % 3 == 0


def test_every_project_has_a_built_page(built):
    for p in PROJECTS:
        page = PAGES[f"case-{p['id']}"]
        assert page_path(page) == f"work/{p['id']}/"
        f = case_file(built, p["id"])
        assert f.is_file(), p["id"]
        html = f.read_text()
        assert f"<title>{p['name']} · Roel Heremans</title>" in html.replace("&amp;", "&")
        assert re.search(r'<meta name="description" content="[^"]{40,}">', html), p["id"]
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S).group(1)
        assert text(h1) == p["name"]
        body = main_of(html)
        assert [text(h) for h in re.findall(r"<h2[^>]*>(.*?)</h2>", body.split('class="case__aside"')[0], re.S)] \
            == ["The challenge", "What I did", "Results"], p["id"]
        dts = [text(d) for d in re.findall(r"<dt>(.*?)</dt>", body, re.S)]
        for label in ("Client", "Question answered", "Stack", "Methods"):
            assert label in dts, (p["id"], label)
        assert ("Key results" in dts) == ("key_results" in p), p["id"]


def test_each_card_links_to_its_page(built):
    work = built / "work" / "index.html"
    html = work.read_text()
    for p in PROJECTS:
        card = re.search(rf'<article class="card project[^"]*" id="{p["id"]}".*?</article>', html, re.S)
        assert card, p["id"]
        links = re.findall(r'<a [^>]*href="([^"]+)"', card.group(0))
        assert links == [f"{p['id']}/"], (p["id"], links)  # one real link, relative
        assert resolve(work, links[0]) == case_file(built, p["id"]).resolve()
        assert "Read the case study" in card.group(0)
    assert 'class="card project project--wide" id="spryfox"' in html


def test_each_redirect_goes_to_its_case_page(built):
    old = {"Electrolux": "electrolux", "PoliticalMonitor": "political-monitor", "bef4U": "bef4u",
           "fbeta": "fbeta", "sniffers": "sniffers", "uptime": "uptime"}
    for name, slug in old.items():
        f = built / "project" / name / "index.html"
        target = re.search(r'<meta http-equiv="refresh" content="0; url=([^"]+)">', f.read_text()).group(1)
        assert target == f"../../work/{slug}/", name
        assert resolve(f, target) == case_file(built, slug).resolve(), name


def test_every_case_page_in_sitemap(built):
    locs = set(re.findall(r"<loc>([^<]+)</loc>", (built / "sitemap.xml").read_text()))
    for p in PROJECTS:
        assert f"{PREVIEW_BASE}work/{p['id']}/" in locs, p["id"]


def test_quotes_only_on_three_projects(built):
    quoted = {"uptime": "Duncan McNicholl, Co-founder & CEO, Uptime Global",
              "political-monitor": "Caspar Pille, Co-founder & CEO, Polpo",
              "sniffers": "Kris Huybs, ICT Director, Intero – The Sniffers"}
    assert {p["id"] for p in PROJECTS if "quote" in p} == set(quoted)
    for p in PROJECTS:
        body = main_of(case_file(built, p["id"]).read_text())
        assert body.count("<blockquote>") == (1 if p["id"] in quoted else 0), p["id"]
        if p["id"] in quoted:
            assert quoted[p["id"]] in text(body)
            assert p["quote"]["text"] in text(body)


def test_engagement_labels(built):
    body = text(main_of(case_file(built, "spryfox").read_text()))
    assert "Direct client" in body
    assert "via Proxify" not in body
    for slug in ("bef4u", "electrolux", "uptime", "political-monitor"):
        assert "via Proxify" in text(main_of(case_file(built, slug).read_text())), slug
    for slug in ("fbeta", "sniffers"):
        b = text(main_of(case_file(built, slug).read_text()))
        assert "via Proxify" not in b and "Direct client" not in b, slug
    assert "Direct client" in text((built / "work" / "index.html").read_text())


def test_exact_key_numbers(built):
    want = {
        "spryfox": ["604,000", "84%", "0.91", "0.50", "75% precision", "256 dimensions",
                    "Oct 2024 to May 2025"],
        "electrolux": ["4.2%", "176,735", "below 14%", "45,000+ employees", "founded 1918"],
        "sniffers": ["+18.47%", "+162.74%", "−5.11%", "−45.13%", "−100%", "46.23%",
                     "Brunei LNG", "150–200 employees"],
        "fbeta": ["50+ benchmark questions", "30–50 employees", "Kendall tau"],
        "bef4u": ["founded 2018", "10+ employees"],
        "uptime": ["founded 2019"],
        "political-monitor": ["founded 2017", "15+ employees"],
    }
    for slug, numbers in want.items():
        body = text(main_of(case_file(built, slug).read_text()))
        for n in numbers:
            assert n in body, (slug, n)


def test_footer_nav_all_work_prev_next(built):
    root = built.resolve()
    for i, p in enumerate(PROJECTS):
        f = case_file(built, p["id"])
        nav = re.search(r'<nav class="[^"]*case-nav".*?</nav>', f.read_text(), re.S).group(0)
        all_work = re.search(r'href="([^"]+)"><span aria-hidden="true">&larr;</span> All work', nav)
        assert all_work and resolve(f, all_work.group(1)) == root / "work" / "index.html"
        prev = re.search(r'href="([^"]+)" rel="prev"', nav)
        nxt = re.search(r'href="([^"]+)" rel="next"', nav)
        assert bool(prev) == (i > 0) and bool(nxt) == (i < len(PROJECTS) - 1), p["id"]
        if prev:
            assert resolve(f, prev.group(1)) == case_file(built, PROJECTS[i - 1]["id"]).resolve()
        if nxt:
            assert resolve(f, nxt.group(1)) == case_file(built, PROJECTS[i + 1]["id"]).resolve()


def test_every_number_on_a_case_page_comes_from_its_project_data(built):
    """No number can be added in a template: every digit sequence in the case content (hero,
    body, side panel, quote; not the prev/next nav or the shared CTA) is in that project's data."""
    for p in PROJECTS:
        html = main_of(case_file(built, p["id"]).read_text())
        content = html.split('<nav class="section', 1)[0]
        data_numbers = set(re.findall(r"\d+", repr(p)))
        page_numbers = set(re.findall(r"\d+", text(content)))
        assert page_numbers, p["id"]
        assert page_numbers <= data_numbers, (p["id"], page_numbers - data_numbers)
