"""URL helpers: every page lives at /<slug>/ ("" = home); all internal links are relative."""
import posixpath


def page_path(page):
    """Output directory of `page` relative to the site root ("" = home), with trailing slash."""
    slug = page["slug"]
    return f"{slug}/" if slug else ""


def rel(from_path, to_path):
    """Relative URL from directory `from_path` to `to_path` (both relative to the site root).

    Directories end with "/" ("" is the root); the result keeps that trailing slash.
    A "#anchor" suffix on `to_path` is kept.
    """
    to_path, hash_, anchor = to_path.partition("#")
    is_dir = to_path == "" or to_path.endswith("/")
    r = posixpath.relpath("/" + to_path, "/" + from_path)
    r = "./" if r == "." else (r + "/" if is_dir else r)
    return r + hash_ + anchor
