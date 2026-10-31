# Editable content for the site. Change these and run build.py to regenerate output.
#
# English only: every visible value is a plain string. "{email}" in a text can be turned
# into a mailto link with the `with_email` helper (partials/helpers.html.j2).

# ── Earlier projects ──
# One entry per project. The same data drives the card on /work/ (meta, name, text) and the
# case-study page at /work/<id>/ (everything else; template case-study.html.j2, one page per
# entry, added to CONTENT["pages"] at the bottom of this file). Order = card order = the
# previous/next links on the case pages. `id` is also the card's anchor on /work/.
# Facts come only from docs/superpowers/specs/2026-10-31-case-study-pages.md: copy numbers
# exactly. `wide`: the card spans the whole grid row (keeps the 3-column grid balanced).
# `engagement`, `period`, `key_results` and `quote` are optional.
PROJECTS = [
    {
        "id": "spryfox",
        "name": "SpryFox",
        "wide": True,
        "meta": "Insurance · text classification",
        "text": "Sorted free-text veterinary invoice lines into insurance coverage codes, with a "
                "confidence score that sends uncertain lines to a human. 84% of predictions correct.",
        "industry": "Insurance analytics",
        "engagement": "Direct client",
        "lede": "Reading veterinary invoices line by line, with a model that knows how sure it is.",
        "description": "SpryFox case study: veterinary invoice lines classified into pet insurance "
                       "coverage codes with biomedical embeddings and calibrated confidence. "
                       "84% of predictions correct.",
        "challenge": [
            "Each line on a veterinary invoice is free text, such as \"Canine Junior Bloodwork "
            "Profile\" or \"Leptospirosis Vaccine - 1 year\". For pet insurance claims, every line "
            "needs a coverage code and a type: wellness, illness or accident.",
        ],
        "did": [
            "I turned the invoice lines into biomedical sentence embeddings with BioLORD-2023-C, "
            "which I compared with BioBERT and all-MiniLM-L6-v2. I reduced them to 256 dimensions "
            "with UMAP and trained PyTorch MLP and LightGBM classifiers.",
            "I calibrated the predicted probabilities and built precision-targeted variants, one "
            "tuned for 75% precision, so the model can say how sure it is. A confidence-breakpoint "
            "analysis decides which lines are automated and which go to a human.",
            "I tracked the experiments in Neptune.ai and also tested LLM prompting with DSPy.",
        ],
        "results": [
            "The model scored about 604,000 invoice lines, and 84% of its predictions were correct. "
            "The average confidence is 0.91 on correct predictions versus 0.50 on wrong ones. That "
            "gap makes a clean threshold for routing uncertain lines to a human reviewer.",
        ],
        "client": "Insurance analytics (pet insurance claims)",
        "period": "Oct 2024 to May 2025",
        "question": "Which coverage code does each line on a veterinary invoice belong to, and is "
                    "it wellness, illness or accident?",
        "stack": "Python, PyTorch, LightGBM, sentence-transformers, UMAP, Neptune.ai, DSPy, Poetry",
        "methods": "Text embeddings, dimensionality reduction, multi-class classification, "
                   "probability calibration, precision/recall threshold tuning",
        "key_results": [
            "About 604,000 invoice lines scored",
            "84% of predictions correct",
            "Average confidence 0.91 on correct predictions versus 0.50 on wrong ones",
        ],
    },
    {
        "id": "bef4u",
        "name": "Bef4U",
        "meta": "Energy · anomaly detection",
        "text": "Online anomaly detection on electricity use in shopping malls: a "
                "sliding-window XGBoost model with z-score alerts.",
        "industry": "Energy efficiency",
        "engagement": "via Proxify",
        "lede": "Flagging abnormal electricity consumption in two shopping malls as the readings "
                "arrive.",
        "description": "Bef4U case study: online anomaly detection on the electricity consumption "
                       "of two shopping malls with a sliding-window XGBoost model and residual "
                       "z-scores.",
        "challenge": [
            "Bef4U needed to detect abnormal electricity consumption in two shopping malls.",
        ],
        "did": [
            "I used an online approach with a sliding training window and testing window, "
            "predicting the next sample outside both windows.",
            "At each step an XGBoost model is trained on the training window, and a z-score on the "
            "residual flags the anomalies.",
        ],
        "results": [
            "An online anomaly detector: at each step an XGBoost model predicts the next reading, "
            "and a z-score on the residual flags readings that fall outside the expected range.",
        ],
        "client": "Sombreffe, Belgium · founded 2018 · environmental services (energy efficiency) "
                  "· 10+ employees",
        "question": "Which consumption readings are abnormal, as they arrive?",
        "stack": "Python, XGBoost",
        "methods": "Sliding-window online learning, residual z-score anomaly detection",
    },
    {
        "id": "electrolux",
        "name": "Electrolux",
        "meta": "Appliances · forecasting",
        "text": "Forecast service call ratios during the warranty period with Markov Random "
                "Fields. 4.2% MAPE for food preservation.",
        "industry": "Household appliances",
        "engagement": "via Proxify",
        "lede": "Forecasting next month's warranty service calls for every product group.",
        "description": "Electrolux case study: forecasting warranty service calls with Markov Random "
                       "Fields regression. 4.2% MAPE for food preservation, below 14% across all "
                       "product hierarchies.",
        "challenge": [
            "During the warranty period, typically one year, Electrolux sends technicians to "
            "customers' homes. The task was to forecast the volume of these service calls from "
            "historical data.",
        ],
        "did": [
            "I built a regression model based on Markov Random Fields, trained on one year of data, "
            "that predicts next month's service calls. The target is the Service Call Ratio (SCR): "
            "service calls normalised by the number of items sold.",
            "An uncertainty band reflects the uncertainty of the sales-volume estimate. I showed the "
            "results across all product hierarchies (product line, group and subgroup) in an "
            "interactive sunburst chart.",
        ],
        "results": [
            "For the food preservation category (mean sales volume 176,735 items per month), the "
            "Mean Absolute Percentage Error on the SCR is 4.2%. Across all product hierarchies the "
            "MAPE stays below 14%.",
        ],
        "client": "Stockholm, Sweden · founded 1918 · household appliances · 45,000+ employees",
        "question": "How many warranty service calls should we expect next month, per product "
                    "group?",
        "stack": "Python",
        "methods": "Markov Random Fields regression, MAPE evaluation, uncertainty bands",
        "key_results": [
            "4.2% MAPE on the SCR for food preservation (mean sales volume 176,735 items per month)",
            "Below 14% MAPE across all product hierarchies",
        ],
    },
    {
        "id": "uptime",
        "name": "Magenta Insight / Uptime",
        "meta": "Water · sensors",
        "text": "Detected when rural well pumps were used from temperature sensors, with a "
                "tuning dashboard and a batch engine.",
        "industry": "Rural water",
        "engagement": "via Proxify",
        "lede": "Reading hand-pump use from the temperature sensor on a well.",
        "description": "Magenta Insight / Uptime case study: detecting when, how often and how long "
                       "rural hand pumps were used, from well temperature sensors.",
        "challenge": [
            "When people pump water, it flows over a temperature sensor on the well. If ambient and "
            "groundwater temperatures differ, this causes a sudden temperature change.",
            "The sensors are read out every few months, so the analysis is offline.",
        ],
        "did": [
            "I built two detection methods. The first extracts local extrema with the slope "
            "profile. The second decomposes the signal into trend, seasonality and residual; the "
            "residual identifies pump use.",
            "I also built a Dash dashboard for quick visualisation and parameter tuning, and a batch "
            "engine that processes many sensor files at once.",
        ],
        "results": [
            "A report per pump with the number of pump uses, the longest and shortest use, and the "
            "start and stop times of each use.",
            "Both methods agree well with ground truth where ambient and water temperatures differ. "
            "When they become similar, detection from temperature alone is not possible, and the "
            "dashboard shows this.",
        ],
        "client": "Oxford, United Kingdom · founded 2019 · rural water maintenance services",
        "question": "When, how often and how long was each hand pump used?",
        "stack": "Python, Dash",
        "methods": "Time-series decomposition, extrema and slope analysis, batch processing",
        "quote": {
            "text": "Roel was great. He seamlessly fit into our team and exceeded expectations "
                    "almost immediately. He's built exactly what we need quickly and effectively.",
            "author": "Duncan McNicholl",
            "role": "Co-founder & CEO, Uptime Global",
        },
    },
    {
        "id": "political-monitor",
        "name": "Your Political Monitor",
        "meta": "Politics · LLM",
        "text": "A web app that summarises political documents and PDFs with an open LLM, "
                "using LangChain map-reduce for long texts.",
        "industry": "Political information",
        "engagement": "via Proxify",
        "lede": "Summarising political documents at ChatGPT-level quality, without ChatGPT.",
        "description": "Your Political Monitor case study: a demo web app that summarises political "
                       "documents and PDFs with an open LLM and LangChain map-reduce.",
        "challenge": [
            "Polpo wanted a web-app demo where clients paste text or upload a PDF and get a "
            "summary, at ChatGPT-level quality and speed but without using ChatGPT.",
        ],
        "did": [
            "I researched which pretrained open LLM to use. Then I analysed LangChain's Map-Reduce "
            "and Refine strategies, so long documents can be summarised too.",
            "I built the demo web app. It shows the summary, the number of words generated and the "
            "time taken.",
        ],
        "results": [
            "A demo web app: the user opens a link, enters or uploads a text and gets the summary, "
            "together with the number of words generated and the time it took.",
        ],
        "client": "Polpo · Amsterdam, Netherlands · founded 2017 · political information "
                  "· 15+ employees",
        "question": "Can we summarise political documents well without ChatGPT?",
        "stack": "Python, LangChain, open-source LLM",
        "methods": "LLM selection, map-reduce and refine summarisation",
        "quote": {
            "text": "We are very happy with the work Roel has delivered. He communicates well, does "
                    "not shy away from challenges, and has a real problem-solving mindset! A great "
                    "addition to any team!",
            "author": "Caspar Pille",
            "role": "Co-founder & CEO, Polpo",
        },
    },
    {
        "id": "fbeta",
        "name": "fbeta",
        "meta": "Consulting · LLM",
        "text": "Scored how well LLM answers agree with expert answers on 50+ benchmark questions, "
                "to pick the best model.",
        "industry": "Business consulting",
        "lede": "Finding the LLM whose answers come closest to the experts.",
        "description": "fbeta case study: scoring LLM answers against subject-matter experts with "
                       "BERT similarity and ranking the models with Kendall tau.",
        "challenge": [
            "fbeta needed to score how well machine-generated answers agree with the answers of "
            "subject-matter experts, to pick the LLM that gives the best answers on a set of 50+ "
            "benchmark questions.",
        ],
        "did": [
            "I compared evaluation techniques. BERT sentence similarity and BERT embedding "
            "similarity were the two most promising.",
            "I used Kendall tau to rank which LLM agreed best with the experts.",
        ],
        "results": [
            "BERT sentence similarity and BERT embedding similarity came out as the two most "
            "promising measures, and Kendall tau then ranked the LLMs by how well they agreed with "
            "the experts.",
        ],
        "client": "Berlin, Germany · founded 2014 · business consulting and services "
                  "· 30–50 employees",
        "question": "Which LLM answers most like our experts?",
        "stack": "Python, BERT",
        "methods": "Semantic similarity scoring, rank correlation (Kendall tau), LLM benchmarking",
    },
    {
        "id": "sniffers",
        "name": "Intero – The Sniffers",
        "meta": "Energy · computer vision",
        "text": "Improved the deep learning models that detect and read text in piping diagrams "
                "(P&IDs). True positives up between +18.47% and +162.74%.",
        "industry": "Energy, oil & gas",
        "lede": "Reading symbols and text in piping diagrams with deep learning.",
        "description": "Intero – The Sniffers case study: Faster R-CNN text detection and fine-tuned "
                       "TrOCR for P&ID diagrams. True positives up between +18.47% and +162.74%.",
        "challenge": [
            "The task was to improve the deep learning models that detect and read symbols and "
            "text in Piping and Instrumentation Diagrams (P&IDs).",
        ],
        "did": [
            "I optimised a Faster R-CNN with a ResNet-50 backbone for text detection in complex "
            "P&IDs.",
            "For text recognition I fine-tuned Microsoft's TrOCR (Transformer OCR) on "
            "domain-specific P&ID text.",
        ],
        "results": [
            "After retraining, true positives went up between +18.47% and +162.74% across models, "
            "and false positives went down between −5.11% and −45.13%.",
            "False negatives went down sharply in three cases, by −100% for the Brunei LNG model. "
            "The mean character error rate went down by up to 46.23%.",
        ],
        "client": "Balen, Belgium · founded 1991 · energy, oil & gas · 150–200 employees",
        "question": "Can we read P&ID diagrams automatically and accurately?",
        "stack": "Python, Faster R-CNN (ResNet-50), TrOCR",
        "methods": "Object detection, OCR fine-tuning, error analysis (TP/FP/FN, character error "
                   "rate)",
        "key_results": [
            "True positives up between +18.47% and +162.74% across models",
            "False positives down between −5.11% and −45.13%",
            "False negatives down sharply in three cases, by −100% for the Brunei LNG model",
            "Mean character error rate down by up to 46.23%",
        ],
        "quote": {
            "text": "Roel consistently excelled in completing the tasks assigned to him. He "
                    "demonstrated a high degree of independence in his work, consistently "
                    "delivering on time while maintaining excellent communication throughout the "
                    "process. I am very satisfied with his entire work ethic.",
            "author": "Kris Huybs",
            "role": "ICT Director, Intero – The Sniffers",
        },
    },
]

CONTENT = {
    # True = GitHub Pages test site: every page gets <meta name="robots" content="noindex">.
    # SITE_ENV=production (see build.py) turns it off.
    "preview": True,
    "site_name": "Roel Heremans",
    "site_url": "https://www.roel-heremans.com/",
    # Base URL used instead of site_url while preview is True (GitHub Pages test site).
    "preview_url": "https://roel-heremans.github.io/RoelHeremans-Site/",
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
            # The h1 is built from CONTENT["home"]["hero"] (with the struck-through "months");
            # this is its plain text, as read without the struck word.
            "heading": "Your analytics question, answered in days. Every number checked by hand.",
            "description": "I solve analytics problems with Claude Code at AI speed, then verify "
                           "every number by hand against your source data. Physicist turned data "
                           "scientist, 20+ years in industry.",
            "nav": "Home",
            "in_nav": False,
        },
        {
            "id": "approach",
            "template": "approach.html.j2",
            "slug": "approach",
            "title": "Approach",
            "heading": "AI does the heavy lifting. I do the checking.",
            "description": "How I work: scope, build with Claude Code, verify every number by hand, "
                           "deliver code and documentation you own.",
            "nav": "Approach",
            "in_nav": True,
        },
        {
            "id": "work",
            "template": "work.html.j2",
            "slug": "work",
            "title": "Work",
            "heading": "Recent projects",
            "description": "Selected analytics projects: Best Way Healthcare, Impala Studios "
                           "severe-weather triggers with GraphCast, and earlier work in energy, "
                           "appliances, water, politics and healthcare.",
            "nav": "Work",
            "in_nav": True,
        },
        {
            "id": "about",
            "template": "about.html.j2",
            "slug": "about",
            "title": "About",
            "heading": "From particle physics to production analytics",
            "description": "Background of Roel Heremans: PhD in elementary particle physics, "
                           "9 years at the Royal Military Academy, AGT International, now an "
                           "independent data scientist working AI-first with Claude Code.",
            "nav": "About",
            "in_nav": True,
        },
        {
            "id": "contact",
            "template": "contact.html.j2",
            "slug": "contact",
            "title": "Contact",
            "heading": "Bring me your analytics question",
            "description": "Send a short email. I reply within two working days with whether I "
                           "can help, a rough plan and a fixed quote. I prefer to be paid in Bitcoin.",
            "nav": "Contact",
            "in_nav": True,
        },
    ],
    # Old Framer paths (at the site root) -> a page of the new site (the /project/* ones go to
    # their case-study page), optionally with an #anchor ({"page": id, "anchor": "id-on-that-page"}). Each becomes a small redirect page.
    "redirects": {
        "project/Electrolux": {"page": "case-electrolux"},
        "project/PoliticalMonitor": {"page": "case-political-monitor"},
        "project/bef4U": {"page": "case-bef4u"},
        "project/fbeta": {"page": "case-fbeta"},
        "project/sniffers": {"page": "case-sniffers"},
        "project/uptime": {"page": "case-uptime"},
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
        "step": "Step",
        "redirect_text": "This page has moved:",
        # Case-study pages and the cards on /work/.
        "case_link": "Read the case study",
        "case_challenge": "The challenge",
        "case_did": "What I did",
        "case_results": "Results",
        "case_client": "Client",
        "case_period": "Period",
        "case_question": "Question answered",
        "case_stack": "Stack",
        "case_methods": "Methods",
        "case_key_results": "Key results",
        "case_quote": "In the client's words",
        "case_all": "All work",
        "case_prev": "Previous",
        "case_next": "Next",
    },
    "footer_tagline": "AI-accelerated, human-verified analytics.",
    "footer_location": "Madeira, Portugal",

    # ── Images (tools/prepare_images.py makes these from original/images/). ──
    "images": {
        "portrait_hero": {"src": "assets/img/roel-portrait-hero.jpg", "w": 2000, "h": 1334,
                          "alt": "Roel Heremans smiling in front of a weathered wooden door"},
        "portrait_square": {"src": "assets/img/roel-portrait-square.jpg", "w": 1200, "h": 1200,
                            "alt": "Portrait of Roel Heremans"},
        "family": {"src": "assets/img/roel-family.jpg", "w": 1200, "h": 846,
                   "alt": "Roel with his family, all dressed in white"},
    },

    # ── Shared blocks ──
    # The four steps of the method. Home shows step, name and "who"; Approach adds the text.
    "steps": [
        {"name": "Scope", "who": "you + me",
         "text": "We pin down the business question, the decision it feeds, and what \"correct\" "
                 "looks like. I get read access to your data and nothing more."},
        {"name": "Build", "who": "claude code, directed by me",
         "text": "Queries, models, pipelines and dashboards are written quickly with Claude Code, "
                 "under my design and in your stack."},
        {"name": "Verify", "who": "me, by hand",
         "text": "I reconcile every headline number against the source, test edge cases and "
                 "challenge results that look too good. Anything that fails goes back to step 2."},
        {"name": "Deliver", "who": "you own it",
         "text": "You get readable code, a refreshable dashboard or report, and plain-English notes "
                 "on definitions, assumptions and limits."},
    ],
    "hand_tested": {
        "eyebrow": "Hand-tested",
        "heading": "What “hand-tested” means",
        "items": [
            "Totals are reconciled against the raw source system, not against the AI's own output.",
            "Key figures are re-derived a second, independent way.",
            "Individual records are traced end to end through the pipeline.",
            "Effects are checked for confounders, such as a product launch or price change, "
            "before they are called a result.",
            "Every definition and assumption is written down, so your team can challenge it.",
        ],
    },
    # Closing call to action (Home, Approach, Work, About).
    "cta": {
        "eyebrow": "Contact",
        "heading": "Bring me your analytics question",
        "text": "Send a short email. I reply within two working days with whether I can help, "
                "a rough plan and a fixed quote.",
        "button": "Send me your question",
    },
    "bitcoin": {
        "eyebrow": "Payment",
        "heading": "I prefer to be paid in Bitcoin",
        "text": "Quotes and invoices are in euros. Settle them in bitcoin at the exchange rate on "
                "the invoice date.",
        "items": [
            "On-chain or Lightning, whichever suits you",
            "A fresh payment address comes with each invoice, so no address is published on this site",
            "Bank transfer in EUR is possible if your company requires it",
        ],
        "note": "price in EUR · settle in BTC",
        # Home: the short note that links to the full section on Contact.
        "home_link": "Payment details",
    },

    # ── Home ──
    "home": {
        "hero": {
            "eyebrow": "Taking on new analytics projects",
            # h1: before + struck-through old word + new word (gold italic) + after.
            "before": "Your analytics question, answered in",
            "old": "months",
            "new": "days",
            "after": ". Every number checked by hand.",
            "lead": "I'm a physicist turned data scientist with 20+ years in industry. I use Claude "
                    "Code to build analyses, pipelines and dashboards at AI speed. Then I verify the "
                    "results myself, line by line, against your source data. You get the speed of AI "
                    "without its hallucinations.",
            "primary": "Send me your question",
            "secondary": "See recent work",
        },
        # The "verification log" card next to the hero. tag: claude | roel | flag.
        "log": {
            "label": "Example verification log for a churn analysis",
            "file": "verification-log.md",
            "marker": "example",
            "lines": [
                {"tag": "claude", "text": "Drafted SQL for weekly churn cohorts"},
                {"tag": "roel", "text": "Re-counted active customers in the source table →",
                 "ok": "totals match"},
                {"tag": "roel", "text": "Checked 20 customers by hand, one by one"},
                {"tag": "flag", "text": "\"Churned\" included customers who reached their goal"},
                {"tag": "claude", "text": "Split churn into goal-met vs. genuine churn"},
                {"tag": "roel", "text": "Re-ran checks, documented the definition"},
            ],
            "status": "status:",
            "status_value": "verified, ready for the client",
        },
        "facts": {
            "label": "Key facts",
            "items": [
                {"value": "20+ years", "text": "industrial data science"},
                {"value": "50+ projects", "text": "in energy, health, weather, sport, defence"},
                {"value": "PhD", "text": "elementary particle physics"},
            ],
        },
        "method": {
            "eyebrow": "How I work",
            "heading": "AI does the heavy lifting. I do the checking.",
            "button": "How I work, step by step",
        },
        "work": {
            "eyebrow": "Selected work",
            "heading": "Recent projects",
            "button": "Read the case study",
            "all": "All projects",
        },
    },

    # ── Approach ──
    "approach": {
        "eyebrow": "How I work",
        "lead": "An AI coding assistant can write in an afternoon what used to take a team a few "
                "weeks. It can also be confidently wrong. My job is to make sure it isn't, before "
                "anything reaches your board or your customers.",
        "steps": {"eyebrow": "The method", "heading": "Four steps"},
        "compare": {
            "eyebrow": "Compared",
            "heading": "What changes for you",
            "columns": ["", "Typical project", "With me"],
            "rows": [
                ["Team", "Several analysts and engineers", "One senior data scientist"],
                ["First results", "Weeks to months", "Days"],
                ["Cost", "Team day rates", "A fraction of that"],
                ["Accuracy", "Depends on review time", "Every number checked"],
                ["Handover", "Often a slide deck", "Code, docs and a live dashboard"],
            ],
        },
        "services": {
            "eyebrow": "What I do",
            "heading": "Typical engagements",
            "items": [
                {"name": "Dashboards that refresh themselves",
                 "text": "Scheduled pipelines from your warehouse (BigQuery, Fabric, Databricks, SQL) "
                         "into one shareable dashboard."},
                {"name": "Churn, retention and cohorts",
                 "text": "Who stays, who leaves and why, with definitions your finance team agrees with."},
                {"name": "Pricing and demand",
                 "text": "Price response models and break-even calculators for real decisions."},
                {"name": "Campaign and experiment review",
                 "text": "Did the campaign or geo test actually work? An independent, honest read-out."},
                {"name": "Forecasting and anomaly detection",
                 "text": "Time series, sensors and event triggers that fire alerts when they matter."},
                {"name": "Text and LLM analytics",
                 "text": "Classify free-text notes, reviews and documents at scale, with measured accuracy."},
            ],
        },
    },

    # ── Work ──
    "work": {
        "eyebrow": "Selected work",
        "featured": [
            {
                "id": "best-way-healthcare",
                "chips": ["Current", "Healthcare · Retail pharmacy"],
                "live": True,
                "name": "Best Way Healthcare",
                # Confidential client: no figures, no patient data, no internal names.
                "paragraphs": [
                    "Data scientist for the commercial and clinical analytics of a UK pharmacy "
                    "group's weight-management service, online and in store.",
                    "I built and maintain an analytics dashboard that refreshes itself several times "
                    "every business day. It covers the full patient journey: acquisition funnel, "
                    "retention and churn, pricing and margins, clinical outcomes, geography and "
                    "promotions.",
                    "Hand-checking pays off here. A rise in \"churn\" turned out to be largely "
                    "patients who had reached their weight goal. An apparent uplift from a promotion "
                    "turned out to be the effect of a new product launch. Both findings changed what "
                    "the business decided to do next.",
                    "Other work includes a price response model, campaign and geo-experiment reviews, "
                    "a transformer-based classifier for pharmacist notes, and planning a patient 360 "
                    "data model in Microsoft Fabric. All of it uses pseudonymised data and is handled "
                    "with GDPR in mind.",
                ],
                "facts": [
                    {"label": "Questions answered",
                     "text": "Who stays on treatment, what price works, which campaigns pay back"},
                    {"label": "Stack",
                     "text": "BigQuery, SQL, Python, Microsoft Fabric, Jira, Claude Code"},
                    {"label": "Methods",
                     "text": "Cohort analysis, survival and churn definitions, multinomial price "
                             "models, geo-experiment evaluation, RoBERTa text classification"},
                ],
            },
            {
                "id": "impala-studios",
                "chips": ["Weather · Consumer apps", "via Proxify"],
                "live": False,
                "name": "Impala Studios: severe-weather triggers with GraphCast",
                "paragraphs": [
                    "Impala Studios publishes NOAA Weather Radar, a US weather app. Their marketing "
                    "team found out about severe weather by reading the news, which was often too "
                    "late to launch a campaign.",
                    "I built a pipeline around Google DeepMind's GraphCast (and GenCast), an AI "
                    "weather model. It pulls ERA5 data from Copernicus and runs daily forecasts on "
                    "RunPod GPUs and a Mac Studio.",
                    "On top of the forecasts I wrote physics-based detectors for hurricanes, severe "
                    "precipitation, and storm cells and supercells. When an event crosses its "
                    "thresholds, a trigger sends a validated JSON alert to Impala's alerts API and to "
                    "Slack. It includes event type, intensity, location and time window, so marketing "
                    "can act before the event reaches mainstream media.",
                    "Forecasts are evaluated against observed data, and the triggers have dry-run "
                    "mode, retries and logging so they can be trusted in production.",
                ],
                # Shown as a row of boxes with arrows; `trigger` is highlighted.
                "pipeline": {
                    "label": "Trigger pipeline",
                    "steps": ["ERA5 / CDS", "GraphCast", "Event detectors", "Trigger",
                              "Alerts API + Slack"],
                    "trigger": "Trigger",
                },
                "facts": [
                    {"label": "Events detected",
                     "text": "Hurricanes · severe precipitation · storm cells and supercells"},
                    {"label": "Stack",
                     "text": "JAX, GraphCast/GenCast, xarray, Python, RunPod, cron, REST API, Slack"},
                ],
            },
        ],
        "earlier": {
            "eyebrow": "Before that",
            "heading": "Earlier projects",
            # Cards and case pages read the same list (PROJECTS, top of this file).
            "items": PROJECTS,
        },
    },

    # ── About ──
    "about": {
        "eyebrow": "Background",
        "lead": "A physicist's habit is to distrust a result until it has been checked another way. "
                "That habit is what makes AI-accelerated work safe to use.",
        "cv": "View my CV (PDF)",
        "timeline": {
            "eyebrow": "Career",
            "heading": "Where I have worked",
            "items": [
                {"where": "Freelance · via Proxify and direct", "role": "Independent data scientist",
                 "text": "Analytics, forecasting and LLM projects for clients in healthcare, weather, "
                         "energy and consumer goods. Now working AI-first with Claude Code."},
                {"where": "AGT International", "role": "Sensor and sports analytics",
                 "text": "Pollution heatmaps from urban sensors feeding healthy-route "
                         "recommendations. Player analytics for the basketball Final Four. A "
                         "sensor-based AI scoring system for Professional Bull Riders."},
                {"where": "Royal Military Academy · 9 years", "role": "Defence research",
                 "text": "Flood detection on synthetic aperture radar, terahertz 3D imaging for "
                         "airport scanners, sonar imaging for sea-mine detection and hyperspectral "
                         "imaging."},
                {"where": "VUB · PhD + 6 years postdoc", "role": "Elementary particle physics",
                 "text": "Doctorate and postdoctoral research in high-energy physics."},
            ],
        },
        "testimonial": {
            "eyebrow": "In a co-worker's words",
            "text": "Roel is an exceptional person in terms of communication and hard work. "
                    "Definitely a problem solver and a very independent worker regarding the tasks "
                    "assigned. Overall, a very kind and fun person, always open to new challenges.",
            "author": "Christos Tsirogiannis, co-worker at Polpo",
        },
        "certificates": {
            "eyebrow": "Learning",
            "heading": "Certificates",
            "items": [
                "Deep Learning Specialization (DeepLearning.AI: neural networks, CNNs, sequence "
                "models, structuring ML projects)",
                "NLP and AI with LLMs (DeepLearning.AI)",
                "Generative Pre-trained Transformers (University of Glasgow)",
                "Google AI Essentials",
            ],
        },
        "outside": {
            "eyebrow": "Outside work",
            "heading": "Family, yoga and kombucha",
            "text": "Outside work, I spend my time with my family, teach Hatha yoga and brew "
                    "kombucha.",
            "quote": "Give the ones you love, wings to fly, roots to come back and reasons to stay.",
            "quote_author": "Dalai Lama",
        },
    },

    # ── Contact ──
    "contact": {
        "eyebrow": "Contact",
        "email_label": "Email",
        "copy_label": "Copy",
        "copied": "Copied",
        "selected": "Selected",
        "mail_app": "Open in mail app",
        "mail_subject": "Analytics project",
        "linkedin_label": "LinkedIn",
        "linkedin_text": "linkedin.com/in/roel-heremans",
        "cv_label": "CV",
        "cv_text": "View my CV (PDF)",
        "include_label": "Useful to include",
        "include": [
            "The question you need answered, and the decision it supports",
            "Where your data lives (warehouse, spreadsheets, an API)",
            "Your deadline",
        ],
    },
    # Served at output/cv/ (build.py copies original/roel-heremans-cv.pdf there).
    "cv_path": "cv/roel-heremans-cv.pdf",
}

# One case-study page per project, at /work/<id>/ (after the five main pages, not in the nav).
CONTENT["pages"] += [
    {
        "id": f"case-{p['id']}",
        "template": "case-study.html.j2",
        "slug": f"work/{p['id']}",
        "title": p["name"],
        "full_title": f"{p['name']} · {CONTENT['site_name']}",
        "heading": p["name"],
        "description": p["description"],
        "nav": p["name"],
        "in_nav": False,
        "project": p["id"],
    }
    for p in PROJECTS
]
