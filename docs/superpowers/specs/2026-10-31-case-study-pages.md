# Case-study pages for earlier projects + SpryFox (2026-10-31)

Addendum to `2026-10-31-roel-heremans-site-design.md` (still binding for style, URLs, rules).

## Goal
Each card under "Earlier projects" on /work/ links to its own case-study page with technical depth,
structured like the two featured case studies (Best Way, Impala): a body of text plus a side panel with
labelled facts. Add SpryFox as a new project, labelled **Direct client**.

## Structure of each case-study page (`/work/<slug>/`)
- Eyebrow chips: industry, engagement (only where given below: "via Proxify" or "Direct client").
- H1 = client name; one-line lede.
- Body sections: **The challenge**, **What I did**, **Results** (results with the exact numbers given below; never round differently, never add numbers).
- Side panel (`dl`, same look as the featured cases): **Client** (HQ · founded · industry · size, only the fields given), **Question answered**, **Stack**, **Methods**, and **Key results** where numbers exist.
- Client quote block where a quote is given (name + role).
- Footer nav: "← All work" plus previous/next project.
- Cards on /work/ get a "Read the case study →" link (whole card clickable is fine, keep one real `<a>`). The card text stays short.
- Grid: 7 earlier projects now. Avoid a lone orphan card in the last row at desktop width (e.g. put SpryFox first as a wide card, or another balanced arrangement).
- Old Framer redirects now go to the case pages: `/project/Electrolux/` → `/work/electrolux/`, `PoliticalMonitor` → `/work/political-monitor/`, `bef4U` → `/work/bef4u/`, `fbeta` → `/work/fbeta/`, `sniffers` → `/work/sniffers/`, `uptime` → `/work/uptime/`. Keep the `id` anchors on /work/ too.
- Add each case page to the sitemap; per-page title "<Client> · Roel Heremans" and a meta description.
- Use only the facts below. Write plain, first-person English, active voice, no em-dash asides.

## Facts per project (the ONLY source)

### SpryFox — slug `spryfox` — **Direct client** — Oct 2024 to May 2025
- Industry: insurance analytics (pet insurance claims). Do not name SpryFox's end client.
- Question answered: Which coverage code does each line on a veterinary invoice belong to, and is it wellness, illness or accident?
- What I did: turned free-text invoice lines (e.g. "Canine Junior Bloodwork Profile", "Leptospirosis Vaccine - 1 year") into biomedical sentence embeddings (BioLORD-2023-C, compared with BioBERT and all-MiniLM-L6-v2), reduced them to 256 dimensions with UMAP, and trained PyTorch MLP and LightGBM classifiers. Calibrated the predicted probabilities and built precision-targeted variants (one tuned for 75% precision), so the model can say how sure it is. A confidence-breakpoint analysis decides which lines are automated and which go to a human. Experiments tracked in Neptune.ai; also tested LLM prompting with DSPy.
- Key results: about 604,000 invoice lines scored; 84% of predictions correct; average confidence 0.91 on correct predictions versus 0.50 on wrong ones, which makes a clean threshold for routing uncertain lines to a human reviewer.
- Stack: Python, PyTorch, LightGBM, sentence-transformers, UMAP, Neptune.ai, DSPy, Poetry.
- Methods: text embeddings, dimensionality reduction, multi-class classification, probability calibration, precision/recall threshold tuning.

### Bef4U — slug `bef4u` — via Proxify
- Client: Sombreffe, Belgium · founded 2018 · environmental services (energy efficiency) · 10+ employees.
- Challenge: detect abnormal electricity consumption in two shopping malls.
- What I did: an online approach with a sliding training window and testing window, predicting the next sample outside both windows. At each step an XGBoost model is trained on the training window and a z-score is computed on the residual to flag anomalies.
- Question answered: Which consumption readings are abnormal, as they arrive?
- Stack: Python, XGBoost. Methods: sliding-window online learning, residual z-score anomaly detection.

### Electrolux — slug `electrolux` — via Proxify
- Client: Stockholm, Sweden · founded 1918 · household appliances · 45,000+ employees.
- Challenge: during the warranty period (typically one year) Electrolux sends technicians to customers' homes. Forecast the volume of these service calls from historical data.
- What I did: a regression model based on Markov Random Fields, trained on one year of data, predicting next month's service calls. The target is the Service Call Ratio (SCR): service calls normalised by the number of items sold. An uncertainty band reflects the uncertainty of the sales-volume estimate. Results across all product hierarchies (product line, group, subgroup) shown in an interactive sunburst chart.
- Key results: 4.2% Mean Absolute Percentage Error on the SCR for the food preservation category (mean sales volume 176,735 items per month); below 14% MAPE across all product hierarchies.
- Question answered: How many warranty service calls should we expect next month, per product group?
- Stack: Python. Methods: Markov Random Fields regression, MAPE evaluation, uncertainty bands.

### Magenta Insight / Uptime — slug `uptime` — via Proxify
- Client: Oxford, United Kingdom · founded 2019 · rural water maintenance services.
- Challenge: when people pump water, it flows over a temperature sensor on the well. If ambient and groundwater temperatures differ, this causes a sudden temperature change. Sensors are read out every few months, so analysis is offline.
- What I did: two detection methods. (1) Local extrema extraction with the slope profile. (2) Decomposition of the signal into trend, seasonality and residual; the residual identifies pump use. Built a Dash dashboard for quick visualisation and parameter tuning, and a batch engine that processes many sensor files at once.
- Results: a report per pump with the number of pump uses, the longest and shortest use, and start and stop times of each use. Both methods agree well with ground truth where ambient and water temperatures differ; when they become similar, detection from temperature alone is not possible, and the dashboard shows this.
- Question answered: When, how often and how long was each hand pump used?
- Stack: Python, Dash. Methods: time-series decomposition, extrema and slope analysis, batch processing.
- Quote: "Roel was great. He seamlessly fit into our team and exceeded expectations almost immediately. He's built exactly what we need quickly and effectively." — Duncan McNicholl, Co-founder & CEO, Uptime Global.

### Your Political Monitor — slug `political-monitor` — via Proxify
- Client: Polpo, Amsterdam, Netherlands · founded 2017 · political information · 15+ employees.
- Challenge: a web-app demo where clients paste text or upload a PDF and get a summary, at ChatGPT-level quality and speed but without using ChatGPT.
- What I did: researched which pretrained open LLM to use, then analysed LangChain's Map-Reduce and Refine strategies so long documents can be summarised too. Built the demo web app, which shows the summary, the number of words generated and the time taken.
- Question answered: Can we summarise political documents well without ChatGPT?
- Stack: Python, LangChain, open-source LLM. Methods: LLM selection, map-reduce and refine summarisation.
- Quote: "We are very happy with the work Roel has delivered. He communicates well, does not shy away from challenges, and has a real problem-solving mindset! A great addition to any team!" — Caspar Pille, Co-founder & CEO, Polpo.

### fbeta — slug `fbeta` — (no engagement label)
- Client: Berlin, Germany · founded 2014 · business consulting and services · 30–50 employees.
- Challenge: score how well machine-generated answers agree with subject-matter-expert answers, to pick the LLM that gives the best answers on a set of 50+ benchmark questions.
- What I did: compared evaluation techniques. BERT sentence similarity and BERT embedding similarity were the two most promising. Used Kendall tau to rank which LLM agreed best with the experts.
- Question answered: Which LLM answers most like our experts?
- Stack: Python, BERT. Methods: semantic similarity scoring, rank correlation (Kendall tau), LLM benchmarking.

### Intero – The Sniffers — slug `sniffers` — (no engagement label)
- Client: Balen, Belgium · founded 1991 · energy, oil & gas · 150–200 employees.
- Challenge: improve deep learning models that detect and read symbols and text in Piping and Instrumentation Diagrams (P&IDs).
- What I did: optimised a Faster R-CNN with ResNet-50 backbone for text detection in complex P&IDs, and fine-tuned Microsoft's TrOCR (Transformer OCR) for text recognition on domain-specific P&ID text.
- Key results after retraining: true positives up between +18.47% and +162.74% across models; false positives down between −5.11% and −45.13%; false negatives down sharply in three cases, by −100% for the Brunei LNG model; mean character error rate down by up to 46.23%.
- Question answered: Can we read P&ID diagrams automatically and accurately?
- Stack: Python, Faster R-CNN (ResNet-50), TrOCR. Methods: object detection, OCR fine-tuning, error analysis (TP/FP/FN, character error rate).
- Quote: "Roel consistently excelled in completing the tasks assigned to him. He demonstrated a high degree of independence in his work, consistently delivering on time while maintaining excellent communication throughout the process. I am very satisfied with his entire work ethic." — Kris Huybs, ICT Director, Intero – The Sniffers.
