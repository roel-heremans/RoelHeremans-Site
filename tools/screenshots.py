#!/usr/bin/env python3
"""Screenshot every page of the site (1440 and 390 wide), check
phones for horizontal scroll and the desktop header for overflow, and build a
simple gallery review/index.html (review/ is gitignored).

Usage: python tools/screenshots.py [base_url]
  local:  ./build-output.sh && python tools/screenshots.py
          (no URL: serves output/ itself on a free port, with the CORS header
          the web fonts need - see below)
  other:  python tools/screenshots.py https://roel-heremans.github.io/RoelHeremans-Site/

The page is shown in a srcdoc iframe, so its fonts are cross-origin requests:
they only load when the server sends Access-Control-Allow-Origin (GitHub Pages
does; plain `python -m http.server` does not, and then the fallback font makes
the header measurements meaningless). Hence the built-in server.

Method: each page is fetched, a <base href> to its live URL is added (so CSS,
images and JS load) and it is embedded as a srcdoc iframe of the exact width in
a host page opened by headless Chrome. Chrome headless windows cannot be
narrower than 500px, so the iframe is what gives a true 390px viewport.
  1. Measure pass (--dump-dom): the host reads the page's scrollWidth and full
     height and, at header widths, whether the nav overflows or wraps.
  2. Screenshot pass (--screenshot): iframe as tall as the page, cropped to
     the iframe width with ImageMagick when the window had to be wider.
Exit code 1 if any check fails.
"""
import functools
import html as H
import http.server
import json
import re
import subprocess
import sys
import tempfile
import threading
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from content import CONTENT  # noqa: E402
from paths import page_path  # noqa: E402

SHOT_WIDTHS = {"desktop": 1440, "phone": 390}
HEADER_WIDTHS = [960, 1100, 1260]
CHROME = "google-chrome"
OUT = ROOT / "review"

# Runs in the host page once the iframe has loaded; writes JSON into <body data-m>.
MEASURE_JS = """
var f=document.getElementById('f');
f.onload=function(){setTimeout(function(){
  var d=f.contentDocument, de=d.documentElement, r={sw:de.scrollWidth, cw:de.clientWidth, w:f.clientWidth,
    h:Math.max(de.scrollHeight, d.body.scrollHeight)};
  var wide=[]; d.body.querySelectorAll('*').forEach(function(el){
    var b=el.getBoundingClientRect(); if(b.width&&b.right>de.clientWidth+0.5&&wide.length<5)
      wide.push(el.tagName.toLowerCase()+(el.className&&el.className.baseVal===undefined?'.'+el.className.trim().replace(/\s+/g,'.'):'')+' right='+Math.round(b.right));});
  if(wide.length) r.wide=wide;
    var hi=d.querySelector('.header-inner'), nav=d.querySelector('.site-nav');
  if(hi){r.header_overflow=hi.scrollWidth>hi.clientWidth;}
  if(nav){
    r.nav_visible=getComputedStyle(nav).display!=='none'&&nav.offsetWidth>0;
    var tops={}, multi=[];
    nav.querySelectorAll('li').forEach(function(li){
      if(li.offsetParent===null) return;
      tops[li.offsetTop]=1;
      var a=li.querySelector('a'); if(a&&a.getClientRects().length>1) multi.push(a.textContent.trim());
    });
    r.nav_rows=Object.keys(tops).length; r.nav_multiline=multi;
  }
  document.body.setAttribute('data-m', JSON.stringify(r));
}, 1200)};
"""


def chrome(*args, timeout=180):
    return subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
                           "--hide-scrollbars", *args], capture_output=True, text=True,
                          timeout=timeout)


# Screenshots only: show fade-in ([data-reveal]) content at once. In a page-tall
# iframe the IntersectionObserver sometimes fires after Chrome has captured.
SHOW_REVEALED = ("<style>[data-reveal]{opacity:1!important;transform:none!important;"
                 "transition:none!important}</style>")


# Measure only: body has overflow-x:hidden, which hides a too-wide element from
# scrollWidth here but not always on phones (iOS Safari still scrolls). Lift it so
# the measured scrollWidth shows any real overflow.
UNCLIP = "<style>html,body{overflow-x:visible!important}</style>"


def host_file(page_html, url, width, height, measure):
    extra = UNCLIP if measure else SHOW_REVEALED
    page_html = page_html.replace("<head>", f'<head><base href="{url}">{extra}', 1)
    host = ('<!doctype html><html><body style="margin:0;background:#fff">'
            f'<iframe id=f style="display:block;width:{width}px;height:{height}px;border:0" '
            f'srcdoc="{H.escape(page_html, quote=True)}"></iframe>'
            + (f"<script>{MEASURE_JS}</script>" if measure else "") + "</body></html>")
    f = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8")
    f.write(host)
    f.close()
    return f.name


def measure(page_html, url, width, height=900):
    path = host_file(page_html, url, width, height, measure=True)
    r = chrome(f"--window-size={max(width, 500) + 20},{height}", "--virtual-time-budget=10000",
               "--dump-dom", "file://" + path)
    m = re.search(r"data-m=\"([^\"]+)\"", r.stdout)
    return json.loads(H.unescape(m.group(1))) if m else None


def screenshot(page_html, url, width, height, target):
    path = host_file(page_html, url, width, height, measure=False)
    win_w = max(width, 500)
    chrome(f"--window-size={win_w},{height}", "--virtual-time-budget=10000",
           f"--screenshot={target}", "file://" + path)
    if win_w != width and target.exists():
        subprocess.run(["convert", str(target), "-crop", f"{width}x{height}+0+0", "+repage",
                        str(target)], check=True)


def pages(base):
    for page in CONTENT["pages"]:
        yield page["id"], base + page_path(page)


def main(base):
    base = base.rstrip("/") + "/"
    shots = OUT / "shots"
    shots.mkdir(parents=True, exist_ok=True)
    problems, rows = [], []
    for name, url in pages(base):
        page_html = urllib.request.urlopen(url).read().decode("utf-8")
        figs = []
        for kind, width in SHOT_WIDTHS.items():
            m = measure(page_html, url, width)
            if not m:
                problems.append(f"{name} @{width}: could not measure")
                continue
            if kind == "phone":
                over = m["sw"] > m["cw"] or m["sw"] > width
                state = (f"OVERFLOW scrollWidth={m['sw']} clientWidth={m['cw']} {m.get('wide', [])}"
                         if over else f"ok (scrollWidth={m['sw']} clientWidth={m['cw']})")
                print(f"  scroll @390 {name}: {state}")
                if over:
                    problems.append(f"{name} @390: horizontal scroll ({m['sw']} > {m['cw']}) {m.get('wide', [])}")
            target = shots / f"{name}-{kind}.png"
            screenshot(page_html, url, width, min(m["h"], 16000), target)
            figs.append(f"<figure><figcaption>{kind} {width}px</figcaption>"
                        f"<a href='shots/{target.name}'><img src='shots/{target.name}' loading=lazy></a></figure>")
        rows.append(f"<h2>{name}</h2><p><a href='{url}'>{url}</a></p><div class=r>{''.join(figs)}</div>")

    print("Header check (nav fits on one row, no overflow):")
    url = base + page_path(CONTENT["pages"][0])
    page_html = urllib.request.urlopen(url).read().decode("utf-8")
    for width in HEADER_WIDTHS:
        m = measure(page_html, url, width, 400)
        bad = (not m or m.get("header_overflow") or not m.get("nav_visible")
               or m.get("nav_rows") != 1 or m.get("nav_multiline") or m["sw"] > m["cw"])
        print(f"  @{width}: {'PROBLEM' if bad else 'ok'} {m}")
        if bad:
            problems.append(f"header @{width}: {m}")

    (OUT / "index.html").write_text(
        "<!doctype html><meta charset=utf-8><title>roel-heremans.com review</title><style>"
        "body{font:14px sans-serif;margin:24px}.r{display:flex;gap:24px;align-items:flex-start}"
        "figure{margin:0}figure:first-child{flex:3.7}figure:last-child{flex:1}"
        "img{width:100%;border:1px solid #ccc}</style><h1>roel-heremans.com review</h1><p>"
        + H.escape(base) + "</p>"
        + ("<h2>Problems</h2><ul>" + "".join(f"<li>{H.escape(p)}</li>" for p in problems) + "</ul>"
           if problems else "<p>All checks passed.</p>")
        + "".join(rows), encoding="utf-8")
    print("Wrote", OUT / "index.html")
    for p in problems:
        print("PROBLEM:", p)
    return 1 if problems else 0


class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def log_message(self, *args):
        pass


def serve_output():
    """Serve output/ on a free localhost port in a background thread; returns its URL."""
    if not (ROOT / "output" / "index.html").exists():
        sys.exit("No output/index.html: run ./build-output.sh first.")
    handler = functools.partial(CORSHandler, directory=str(ROOT / "output"))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{server.server_address[1]}/"


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else serve_output()))
