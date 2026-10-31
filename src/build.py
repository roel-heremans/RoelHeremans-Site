"""
Generate output/ (5 pages + one case-study page per project, redirects for old URLs, robots.txt, sitemap.xml, the CV PDF).
Edit src/content.py and run: python src/build.py (from project root)
SITE_ENV=production builds the live site (indexable); anything else builds the noindex test site.
"""
import datetime
import os
import shutil
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from jinja2 import Environment, FileSystemLoader, StrictUndefined, pass_context

from content import CONTENT
from paths import page_path, rel

ROOT = SRC_DIR.parent
TEMPLATES_DIR = SRC_DIR / "templates"
OUT_DIR = ROOT / "output"


def _write(out_dir: Path, path: str, html: str) -> None:
    target = out_dir / path / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")


def redirect_target(target: dict, pages: dict) -> str:
    """Site-root-relative path (with optional #anchor) for a CONTENT["redirects"] target."""
    return page_path(pages[target["page"]]) + (f"#{target['anchor']}" if "anchor" in target else "")


def build(out_dir: Path, content: dict) -> None:
    out_dir = Path(out_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    pages = {p["id"]: p for p in content["pages"]}
    base = content["preview_url"] if content["preview"] else content["site_url"]

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False,
                      undefined=StrictUndefined)

    @pass_context
    def url(ctx, page_id):
        return rel(ctx["path"], page_path(pages[page_id]))

    def asset_exists(path):
        return (ROOT / "assets" / path).is_file()

    env.globals.update(url=url, page_path=page_path, asset_exists=asset_exists)
    year = datetime.date.today().year

    for page in content["pages"]:
        template = env.get_template(page["template"])
        path = page_path(page)
        html = template.render(content=content, page=page, path=path,
                               root=rel(path, ""), year=year, site_base=base)
        _write(out_dir, path, html)
        print(f"  built {path or '/'}")

    redirect = env.get_template("redirect.html.j2")
    for old, target in content["redirects"].items():
        path = f"{old}/"
        target_path = redirect_target(target, pages)
        html = redirect.render(
            content=content, path=path, root=rel(path, ""), site_base=base,
            target_url=rel(path, target_path), canonical=base + target_path,
        )
        _write(out_dir, path, html)
        print(f"  redirect {path} -> {target_path or '/'}")

    if content["preview"]:
        robots = "User-agent: *\nDisallow: /\n"
    else:
        robots = f"User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n"
        # Live site on STRATO (Apache): send http:// and the bare domain to https://www.
        (out_dir / ".htaccess").write_text(
            "RewriteEngine On\n"
            "RewriteCond %{HTTPS} !=on [OR]\n"
            "RewriteCond %{HTTP_HOST} !^www\\. [NC]\n"
            f"RewriteRule ^(.*)$ {base}$1 [R=301,L]\n",
            encoding="utf-8",
        )
    (out_dir / "robots.txt").write_text(robots, encoding="utf-8")

    urls = "".join(f"  <url>\n    <loc>{base}{page_path(p)}</loc>\n  </url>\n"
                   for p in content["pages"])
    (out_dir / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}</urlset>\n",
        encoding="utf-8",
    )

    cv_src = ROOT / "original" / "roel-heremans-cv.pdf"
    cv_out = out_dir / content["cv_path"]
    cv_out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(cv_src, cv_out)
    print(f"  copied {content['cv_path']}")

    assets = ROOT / "assets"
    if assets.is_dir():
        shutil.copytree(assets, out_dir / "assets")
        print("  copied assets/")

    print(f"Done. Output is in {out_dir}")


def content_for_env(environ) -> dict:
    if environ.get("SITE_ENV") == "production":
        return {**CONTENT, "preview": False}
    return CONTENT


def main():
    build(OUT_DIR, content_for_env(os.environ))


if __name__ == "__main__":
    main()
