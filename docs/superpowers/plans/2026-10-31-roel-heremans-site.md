# roel-heremans.com site — implementation plan

Spec: `docs/superpowers/specs/2026-10-31-roel-heremans-site-design.md` (binding authority; read it fully).
Reference implementation: `/home/roel/Documents/PersonalRepos/NinaWebPage` (read-only, never modify it).
Content source: `original/draft/roel-heremans.html`.

## Global Constraints
- Python 3 + Jinja2 static generator; `./build-output.sh` writes `output/`; `pytest -q` must be green after every task.
- Use a local venv: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt` (`.venv/` gitignored, as are `output/`, `review/`, `.pytest_cache/`, `__pycache__/`, `.superpowers/`).
- English only — no i18n, no language switch.
- All colours only in the single `:root` block of `assets/css/styles.css` (test-enforced, as in NinaWebPage).
- Fonts: self-hosted Cormorant Garamond + Inter copied from NinaWebPage `assets/fonts/` (keep OFL.txt).
- Site must work under the GitHub Pages sub-path `/RoelHeremans-Site/` and at a domain root.
- `CONTENT["preview"] = True` → every page has `<meta name="robots" content="noindex">`; `SITE_ENV=production` removes it.
- Never invent facts, figures, clients or testimonials; Best Way Healthcare: no figures, no internal names.
- Commit after each task with a clear message. Do NOT add any Co-Authored-By or "Generated with Claude Code" lines to commits. Do not push.

## Task 1: Scaffold from NinaWebPage
Copy and adapt NinaWebPage's infrastructure into this repo: `requirements.txt`, `build-output.sh`, `.gitignore`,
`src/build.py`, `src/content.py` (skeleton), `src/templates/base.html.j2` + `partials/` (header, footer, helpers, icons),
`assets/css/styles.css`, `assets/fonts/*`, `assets/js/site.js`, `tools/screenshots.py`, `tests/` (conftest, build, css, pages, site_integrity — adapted),
and `.github/workflows/deploy.yml` (build + Pages jobs only; drop the STRATO job, `tools/deploy_strato.py`, `tools/strato_known_hosts` and STRATO tests).
Remove i18n (`src/i18n.py`, DE/EN pairs, lang switch, i18n tests), PayPal and offer-page logic.
Set Roel's colour tokens from the spec. Page list in `CONTENT["pages"]`: home `/`, approach `/approach/`, work `/work/`, about `/about/`, contact `/contact/`, each with a minimal placeholder template that renders through `base.html.j2`.
Keep the redirect mechanism (`CONTENT["redirects"]`) and the robots/sitemap/preview vs production logic.
Done when: build + pytest green, `output/` has the five pages, nav shows Approach · Work · About · Contact + "Start a project" button.

## Task 2: Content and page templates
Move all copy from `original/draft/roel-heremans.html` into `src/content.py` and build the five page templates exactly as the spec's "Pages and URLs" table distributes it, in the sister-site visual language (Cormorant display headings, alternating `--bg`/`--bg-alt` sections, one `--grad-feature` band with light text — use it for the method/“hand-tested” or the CTA band, gold accent).
Includes: hero with struck-through “months” → gold italic “days” (draw-in animation, visible under reduced motion), verification-log card (system mono stack, marked “example”), key facts, 4-step method, hand-tested checklist with `--ok` ticks, comparison table (horizontally scrollable on phones), typical engagements, the two featured case studies with the Impala trigger pipeline row, earlier projects with id anchors (`bef4u`, `electrolux`, `uptime`, `political-monitor`, `fbeta`, `sniffers`), background timeline, the one testimonial, certificates, outside-work note with the Dalai Lama quote (“Give the ones you love, wings to fly, roots to come back and reasons to stay”), contact block with copy button, and the Bitcoin section per spec (Home gets a short Bitcoin note linking to Contact).
Redirects from the spec (`/project/*` → `/work/#…`, `/de/` → `/`). CV: copy `original/roel-heremans-cv.pdf` to `output/cv/roel-heremans-cv.pdf` at build time and link it.
Per-page titles/meta descriptions per spec. Tests: every page renders its key headings, every redirect target anchor exists, CV is in output, Bitcoin section present, no figures in the Best Way block is not testable — skip that.
Image slots (hero portrait, about portrait, family photo) may reference the filenames Task 3 will create: `assets/img/roel-portrait-hero.jpg`, `assets/img/roel-portrait-square.jpg`, `assets/img/roel-family.jpg`; if those files do not exist yet, Task 2 creates temporary placeholders via the Task 3 tool is NOT allowed — instead, Task 2 leaves the image tests to Task 3 and makes the build tolerate missing images.

## Task 3: Images
Adapt NinaWebPage `tools/prepare_images.py` (ImageMagick) to produce from `original/images/`:
`roel-portrait-hero.jpg` (hero crop, ≤2000px), `roel-portrait-square.jpg` (≤1200px), `roel-family.jpg` (≤1200px), JPEG q82;
`og.jpg` 1200×630 (portrait + “Roel Heremans” + “AI-accelerated, human-verified analytics” on the brand gradient), `favicon.png` (serif “RH” in gold on `--brand-deep`).
Commit `original/images/` and the generated `assets/img/`. Wire og/favicon into `base.html.j2`. Add the images test (every image in assets/img is used; referenced images exist).

## Task 4: README and visual review
Write `README.md` modelled on NinaWebPage's (setup, build/test/preview, page structure, editing content, images, colours, visual review, deploy phase 1 to `https://roel-heremans.github.io/RoelHeremans-Site/`, phase 2 open item for roel-heremans.com DNS/hosting, open items incl. German version dropped, Bitcoin address comes per invoice).
Run `python tools/screenshots.py`; fix every reported problem (horizontal scroll at 390px, nav wrapping at 960/1100/1260). Look at the 1440px and 390px shots of all pages and fix visible layout defects (overlaps, clipped text, broken spacing). Report what you changed.
