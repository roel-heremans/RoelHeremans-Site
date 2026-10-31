# roel-heremans.com — site design (2026-10-31)

## Goal
Replace the Framer site at roel-heremans.com with a static site generated from this repo. Built the
same way and in the same visual family as ninasuza.com, realhealthkombucha.com and sattva-reset.com.
The site has one job: get clients to bring Roel analytics problems that he solves with Claude Code.
The pitch: **AI-accelerated, human-verified analytics**. Work gets done much faster and with fewer
people, but Roel tests every number by hand, so AI hallucinations do not reach the client.

Phase 1 (this spec) is a GitHub Pages test site, like NinaSuza-Site:
`https://roel-heremans.github.io/RoelHeremans-Site/` (public repo `roel-heremans/RoelHeremans-Site`,
`noindex` while `CONTENT["preview"]` is True). Phase 2 (DNS / live hosting for roel-heremans.com) is
out of scope. Write it up as an open item in the README.

## Reference implementation: copy it, then adapt
`/home/roel/Documents/PersonalRepos/NinaWebPage` is the template. Read its README,
`docs/superpowers/specs/2026-10-31-ninasuza-site-design.md`, `src/build.py`, `src/content.py`,
`src/templates/**`, `assets/css/styles.css`, `assets/js/site.js`, `tests/**`, `tools/screenshots.py`,
`tools/prepare_images.py` and `.github/workflows/deploy.yml`. Reuse its architecture, conventions and
tests wherever they fit:
- Python + Jinja2 generator: `src/build.py` writes `output/`, and `./build-output.sh` runs it.
- All copy lives in `src/content.py`. Templates live in `src/templates/`, with shared parts in `partials/`.
- `assets/css/styles.css` has ONE `:root` token block. A test fails if any other hex/rgb/hsl colour
  appears in the CSS.
- Self-hosted fonts are copied from NinaWebPage `assets/fonts/` (Cormorant Garamond + Inter, OFL).
- `assets/js/site.js` handles the phone menu and fade-in only.
- `tools/prepare_images.py` uses ImageMagick and turns `original/images/` into `assets/img/`.
  Commit `original/images/` here (only 2 files, about 0.8 MB). Also make `og.jpg`, `favicon.png` and a logo.
- `tools/screenshots.py` is the visual review: 1440px and 390px shots, a horizontal-scroll check and
  the nav-on-one-row check.
- pytest suite: build works, every page renders, internal links/anchors resolve, CSS tokens are
  respected, every image in assets/img is used, redirect pages work, `noindex` is present in preview,
  and the deploy workflow is checked.
- `.github/workflows/deploy.yml`: pytest → build → GitHub Pages. **Drop the STRATO job** and its
  tool, known_hosts and tests.
- The site must work under the `/RoelHeremans-Site/` sub-path on Pages. Do it the way NinaWebPage
  does (relative URLs / base path).

**Differences from NinaWebPage:** English only. Drop i18n, the language switch, the DE/EN pairs and
the i18n tests. Keep the page-list structure (`CONTENT["pages"]`). Drop PayPal and the offer-page tests.

## Visual style (same family as the three sites, Roel's own colour)
Use Nina's/kombucha's system: Cormorant Garamond for the display headings (light weights, with
italic for emphasis), Inter for body text and UI, an off-white base, sections alternating `--bg` /
`--bg-alt`, deep gradient feature bands with light text, a gold accent, 4px radius, generous
whitespace and a subtle fade-in. Roel's brand colour is a deep ink/slate blue that reads as
analytical and calm. The gold accent echoes Bitcoin. Starting tokens (tune them for contrast, small
text must reach ≥ 4.5:1):
- `--brand: #2B4A66`, `--brand-deep: #1B3247`,
  `--grad-feature: linear-gradient(115deg,#14263A 0%,#1B3247 45%,#2B4A66 100%)`
- `--accent: #C9A24A` (gold), plus an `--accent-text` dark enough for small text on light backgrounds
- `--bg: #F7F7F4`, `--bg-alt: #ECEEEF`, `--surface: #FFFFFF`, `--line: #DADFE3`
- `--text: #1D2730`, `--muted: #5C6772`, `--light: #8E98A1`
- a semantic `--ok` green, used only for "verified" ticks

Light theme only, as on the sister sites. One memorable detail goes in the home hero: the headline
"Your analytics question, answered in ~~months~~ *days*.", where "months" is struck through with a
hand-drawn-looking gold line and "days" is set in gold italic. The line draws in once on load, and
the word stays visible with `prefers-reduced-motion`. Next to or under it sits the **verification
log** card from the draft, a small mono-styled panel showing `claude` steps and `roel` checks,
marked "example". Use a system mono stack for it; don't add another webfont.

## Pages and URLs
| Page | URL | Content |
|---|---|---|
| Home | `/` | Hero (pitch + portrait `roel-portrait-door`), key facts, the 4-step method (short), "what hand-tested means", featured work teasers (Best Way, Impala), the Bitcoin note, CTA |
| Approach | `/approach/` | The full method: 4 steps, the hand-tested checklist, a comparison table, typical engagements |
| Work | `/work/` | Featured case studies Best Way Healthcare + Impala Studios (full text), then the earlier projects, each with an `id` anchor |
| About | `/about/` | Background timeline, the testimonial, certificates, "outside work" with the family photo and the Dalai Lama quote |
| Contact | `/contact/` | Email (shown as text + copy button + mailto), LinkedIn, CV, what to include, **Bitcoin payment section** |

Nav: Approach · Work · About · Contact, plus a "Start a project" button that goes to Contact.

Redirects from the old Framer URLs (small redirect pages, the same mechanism as NinaWebPage
`CONTENT["redirects"]`):
- `/project/Electrolux/` → `/work/#electrolux`
- `/project/PoliticalMonitor/` → `/work/#political-monitor`
- `/project/bef4U/` → `/work/#bef4u`
- `/project/fbeta/` → `/work/#fbeta`
- `/project/sniffers/` → `/work/#sniffers`
- `/project/uptime/` → `/work/#uptime`
- `/de/` → `/`

## Content source
Use the copy in `original/draft/roel-heremans.html`. It is reviewed and complete: hero, method,
checks, comparison table, services, both featured case studies, earlier projects, timeline,
testimonial, certificates, contact and Bitcoin. Move it into `src/content.py` and split it across the
pages above. Keep the wording: plain, active voice, first person. Do not invent new facts, figures,
clients or testimonials. The old site's other testimonials were placeholder text, so leave them out.

Rules for the confidential client (Best Way Healthcare):
- No figures, no patient data, no internal names. Describe the work only at the level the draft does.

Facts that may be used: 20+ years in industry, 50+ projects, PhD in elementary particle physics (VUB)
plus 6 years of postdoc, 9 years at the Royal Military Academy, AGT International (urban sensor
pollution heatmaps, basketball Final Four analytics, PBR bull-riding scoring), freelance via Proxify,
the certificates, Hatha yoga teacher, kombucha brewer, family. Email: roel.heremans@gmail.com.
LinkedIn: https://www.linkedin.com/in/roel-heremans/.

CV: copy `original/roel-heremans-cv.pdf` to `output/cv/roel-heremans-cv.pdf` (served from the site,
not from Framer).

### Bitcoin payment section (Contact page, plus a short note on Home)
- Heading: "I prefer to be paid in Bitcoin".
- Quotes and invoices are in euros, settled in bitcoin at the exchange rate on the invoice date.
- On-chain or Lightning.
- A fresh payment address comes with each invoice, so no address is published on the site.
- Bank transfer in EUR is possible if a company requires it.
- Visual: a ₿ glyph in the gold accent, in a card with an accent border.

## Images
- `original/images/roel-portrait-door.jpg` (4898×3266, Roel smiling in front of an old green door):
  hero portrait. Crop it for the hero and use a square/portrait crop on About.
- `original/images/roel-family.jpg` (4764×3358, family in white): About → "Outside work".
- og.jpg 1200×630: the portrait plus the name "Roel Heremans" and "AI-accelerated, human-verified
  analytics" on the brand gradient. favicon.png: a serif "RH" monogram in gold on `--brand-deep`.
  Header wordmark: "Roel Heremans" in Cormorant, set as real text, not an image.
- Do not use client logos.

## SEO / meta
Per-page `<title>` and meta description. Home title: "Roel Heremans · AI-accelerated, human-verified
analytics". Set og tags, canonical to https://www.roel-heremans.com/… (production only), sitemap.xml
and robots.txt, mirroring NinaWebPage's preview/production split (`SITE_ENV=production`).

## Done when
- `./build-output.sh && pytest -q` is all green.
- `python tools/screenshots.py` passes: no horizontal scroll at 390px, and the nav stays on one row at
  960, 1100 and 1260px.
- The README documents setup, build, tests, content editing, images, colours, deploy and open items.
