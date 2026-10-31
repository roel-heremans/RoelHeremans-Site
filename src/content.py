# Editable content for the site. Change these and run build.py to regenerate output.
#
# English only: every visible value is a plain string. "{email}" in a text can be turned
# into a mailto link with the `with_email` helper (partials/helpers.html.j2).

CONTENT = {
    # True = GitHub Pages test site: every page gets <meta name="robots" content="noindex">.
    # SITE_ENV=production (see build.py) turns it off.
    "preview": True,
    "site_name": "Roel Heremans",
    "site_url": "https://www.roel-heremans.com/",
    "meta_description": "Roel Heremans solves analytics problems with Claude Code: "
                        "AI-accelerated, human-verified, every number tested by hand.",
    # Pages, in navigation order. The page lives at /<slug>/ ("" = home).
    # `title`: <title> is "<title> | <site_name>" unless `full_title` is set.
    # `heading`: the one <h1> (placeholder text until the real copy arrives).
    # `description`: meta description (falls back to meta_description). `in_nav`: header link.
    "pages": [
        {
            "id": "home",
            "template": "home.html.j2",
            "slug": "",
            "title": "Home",
            "full_title": "Roel Heremans · AI-accelerated, human-verified analytics",
            "heading": "Your analytics question, answered in days.",
            "nav": "Home",
            "in_nav": False,
        },
        {
            "id": "approach",
            "template": "approach.html.j2",
            "slug": "approach",
            "title": "Approach",
            "heading": "Approach",
            "nav": "Approach",
            "in_nav": True,
        },
        {
            "id": "work",
            "template": "work.html.j2",
            "slug": "work",
            "title": "Work",
            "heading": "Work",
            "nav": "Work",
            "in_nav": True,
        },
        {
            "id": "about",
            "template": "about.html.j2",
            "slug": "about",
            "title": "About",
            "heading": "About",
            "nav": "About",
            "in_nav": True,
        },
        {
            "id": "contact",
            "template": "contact.html.j2",
            "slug": "contact",
            "title": "Contact",
            "heading": "Contact",
            "nav": "Contact",
            "in_nav": True,
        },
    ],
    # Old Framer paths (at the site root) -> a page of the new site, optionally with an
    # #anchor ({"page": id, "anchor": "id-on-that-page"}). Each becomes a small redirect page.
    "redirects": {
        "project/Electrolux": {"page": "work", "anchor": "electrolux"},
        "project/PoliticalMonitor": {"page": "work", "anchor": "political-monitor"},
        "project/bef4U": {"page": "work", "anchor": "bef4u"},
        "project/fbeta": {"page": "work", "anchor": "fbeta"},
        "project/sniffers": {"page": "work", "anchor": "sniffers"},
        "project/uptime": {"page": "work", "anchor": "uptime"},
        "de": {"page": "home"},
    },
    "links": {
        "email": "roel.heremans@gmail.com",
        "linkedin": "https://www.linkedin.com/in/roel-heremans/",
    },
    # Interface texts shared by all pages.
    "ui": {
        "skip": "Skip to content",
        "menu": "Main menu",
        "menu_open": "Open menu",
        "menu_close": "Close menu",
        "footer_nav": "Pages",
        "email": "Email",
        "cta": "Start a project",
        "redirect_text": "This page has moved:",
    },
    "footer_tagline": "AI-accelerated, human-verified analytics.",
}
