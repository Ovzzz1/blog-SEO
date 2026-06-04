# Python for SEO: A Comprehensive Guide for the Non-Developer SEO Consultant

> A practical, opinionated playbook to take an SEO consultant with **zero coding background** from "I've never written a line of code" to "I can build, run, and maintain real Python scripts that replace hours of spreadsheet work, integrate APIs, automate audits, do redirect mappings at scale, cluster keywords semantically, and monitor brand citations across LLMs."

This guide is built on the legacy and current work of the SEO-Python community: JC Chouinard's complete Python-for-SEO course, the late Hamlet Batista's pioneering Search Engine Journal columns, Elias Dabbas's `advertools` ecosystem, Lee Foot's redirect-mapping and semantic-clustering scripts, Greg Bernhardt's importSEM tutorials, Ruth Everett's introductory SearchPilot/SEJ posts, Andreas Voniatis's *Data-Driven SEO with Python* (Apress, 2023), Josh Carty's `google-searchconsole` wrapper, plus canonical sources at Real Python and python.org. Every concept below is in active production use somewhere in the SEO industry today.

---

# SECTION 1 — Python Foundations for a Total Beginner

## 1. What Python actually is

Python is a **general-purpose, interpreted, dynamically-typed programming language** created by Guido van Rossum in 1991. The current major version (Python 3) was released in 2008. "Interpreted" means you do not have to compile your code to a binary first — the Python *interpreter* reads your `.py` file line by line at runtime. That makes the feedback loop fast and friendly, which is why Python dominates data work, scientific computing, ML, and — increasingly — SEO.

Why SEOs love it specifically:

- **Replace Excel for >100K-row datasets.** Excel chokes around the million-row mark and grinds well before that on any non-trivial calculation. pandas DataFrames do not.
- **APIs are first-class.** Every important SEO tool (GSC, GA4, PageSpeed, Ahrefs, SEMrush, DataForSEO, OpenAI, Anthropic) has a REST API; Python's `requests` and official client libraries make pulling that data trivial.
- **A massive open-source SEO toolbox exists already**: `advertools` (Elias Dabbas), `polyfuzz`, `sentence-transformers`, `BeautifulSoup`, `Scrapy`, `google-searchconsole` (Josh Carty), `gspread`.
- **It runs everywhere** — your laptop, Google Colab in a browser, a cron job on a Mac, a GitHub Action in the cloud.

The simplest possible Python program:

```python
print("Hello, SEO")
```

You can run this at a terminal as `python script.py`, paste it into a Jupyter or Colab cell, or type it into the interactive Python REPL. That same one-line philosophy scales — a Python script that crawls 1M URLs, parses each one with BeautifulSoup, and writes the result to a parquet file is recognisably the same shape of code.

## 2. How to run Python — terminal vs Colab vs Jupyter vs VS Code

| Environment | What it is | Pros | Cons | Best for |
|---|---|---|---|---|
| **Google Colab** | A free, hosted Jupyter notebook running on Google's servers. Open `colab.research.google.com` in your browser. | Zero install, free GPU/TPU available, easy sharing (it's a Google Doc for code), pre-installed pandas/numpy. | Sessions die after ~12h idle; uploading large files is fiddly; no native filesystem. | **An SEO consultant's default starting point.** Almost every Python-for-SEO tutorial (Lee Foot's clustering, JC Chouinard's GSC API, Hamlet Batista's intent classification) ships as a Colab. |
| **Jupyter Notebook / JupyterLab** | A locally-installed browser-based notebook. Same `.ipynb` file format as Colab. | Works offline; full filesystem access; persistent. | You have to install Python + Jupyter; no GPU. | Local exploratory analysis on client data you don't want to upload to Google. |
| **VS Code** | A free Microsoft code editor with a first-class Python extension. Supports both `.py` files and `.ipynb` notebooks side-by-side. | Best of both worlds: notebook cells + real IDE features (debugger, Git, terminal). Excellent linting, AI assist via Copilot. | Slightly more setup; intimidating UI at first. | Where you graduate to once you have 5+ scripts and need version control. |
| **Terminal / Command Line** | The raw `python script.py` execution model. | Required for cron-scheduled jobs, GitHub Actions, server deployments, headless crawls. | No interactivity, no inline output. | Production scripts. |

**Recommendation for the consultant:** start in **Google Colab** for weeks 1–4 (zero install friction, all the libraries you need already there), then install **VS Code + Python locally** around week 5 once you want to run things on a schedule and version-control your work. Skip Spyder and PyCharm — they're heavier than you need.

## 3. Installing Python — pip, venv, what `pip install` actually does

If you go local: download the installer from [python.org/downloads](https://www.python.org/downloads/) (3.11 or newer). On macOS check ✅ "Add Python to PATH" during install; on Windows the same.

**`pip`** is Python's package installer. It pulls libraries from PyPI (the Python Package Index — the npm of Python). Running `pip install pandas` downloads pandas + every package it depends on into your Python's `site-packages` directory.

**A virtual environment (`venv`)** is an isolated copy of Python with its own `site-packages`. You make one per project, so your *Client A redirect-mapping* script's exact pinned versions of pandas and polyfuzz don't conflict with your *Client B GSC API* script.

The canonical workflow (per the [official Python packaging guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)):

```bash
# Create a project folder and a virtual env inside it
mkdir client-a-seo && cd client-a-seo
python3 -m venv .venv

# Activate it
source .venv/bin/activate          # Mac/Linux
.venv\Scripts\activate             # Windows PowerShell

# Now any pip install goes ONLY into this folder
pip install pandas requests beautifulsoup4 advertools

# Save your dependencies so the script is reproducible
pip freeze > requirements.txt

# Later, on a new machine:
pip install -r requirements.txt
```

You'll see `(.venv)` prepended to your prompt when the env is active. Run `deactivate` to exit.

**Why this matters for SEO:** when you hand a script to a client or run it inside GitHub Actions, the `requirements.txt` file is what guarantees it works there too.

## 4. Variables and data types

Python has four primitive types you'll use constantly:

```python
url            = "https://example.com/page"   # str  — strings
status_code    = 200                          # int  — whole numbers
load_time_sec  = 1.42                         # float — decimals
is_indexable   = True                         # bool — True or False
```

You don't declare types — Python infers them. You inspect them with `type(url)` → `<class 'str'>`. SEO examples in the wild:

```python
# Everything you scrape from the web starts as a string
title = "Best Running Shoes 2026 | Acme"
print(len(title))                # 33  — handy for title-length checks

# Convert string → int if a CSV cell came in as text
status_str = "404"
status_int = int(status_str)
```

## 5. Lists `[]` and Dictionaries `{}`

A **list** is an ordered, indexable collection. A **dict** is an unordered collection of key→value pairs. They are the bread and butter of every SEO script.

```python
# A list of URLs to check
urls = [
    "https://example.com/",
    "https://example.com/about",
    "https://example.com/contact",
]
print(urls[0])                 # https://example.com/
print(len(urls))               # 3

# A dict mapping URL → status code (a typical scraper output)
status_map = {
    "https://example.com/":         200,
    "https://example.com/old-page": 301,
    "https://example.com/dead":     404,
}
print(status_map["https://example.com/dead"])   # 404

# Loop a dict
for url, code in status_map.items():
    if code != 200:
        print(f"Issue: {url} → {code}")
```

You will see lists of dicts everywhere — it's the natural shape of data returned by REST APIs:

```python
crawl = [
    {"url": "/a", "title": "A", "status": 200},
    {"url": "/b", "title": "B", "status": 301},
]
```

That structure converts directly to a pandas DataFrame with `pd.DataFrame(crawl)`.

## 6. For loops and while loops

A `for` loop runs once per item in an iterable. A `while` loop runs as long as a condition stays `True`. JC Chouinard's intro tutorial illustrates both:

```python
# For loop: check titles for a brand keyword
titles = ["Acme Running Shoes", "Generic Trainers", "Acme Trail Runners"]
for title in titles:
    if "Acme" in title:
        print(f"On-brand: {title}")

# While loop: paginate an API until it stops returning rows
page = 1
while page <= 10:
    print(f"Fetching page {page}")
    page += 1
```

In practice in SEO scripts, `for` loops dominate. A typical pattern: loop URLs → make a request → store result.

## 7. If / elif / else

Conditional logic. The two SEO-canonical examples from Hamlet Batista's "Practical Introduction to Python" SEJ column:

```python
# Status-code triage
if status_code == 404:
    action = "redirect"
elif status_code in (301, 302):
    action = "review chain"
elif status_code >= 500:
    action = "raise with dev"
else:
    action = "ok"

# Title-length QA
title_len = len(title)
if title_len > 60:
    flag = "too long"
elif title_len < 30:
    flag = "too short"
else:
    flag = "ok"
```

Indentation matters — Python uses 4 spaces (no braces). This is enforced by the language, not optional style.

## 8. Functions (`def`)

A function packages reusable logic. The three reasons it matters for SEO:

1. **Reusability** — write the title-length check once, run it on 10K rows.
2. **Testability** — a small function is easy to verify.
3. **Composability** — small functions stack into pipelines.

```python
def title_quality(title: str, min_len: int = 30, max_len: int = 60) -> str:
    """Return a quality label for an SEO title tag."""
    if not title:
        return "missing"
    n = len(title)
    if n > max_len:
        return "too long"
    if n < min_len:
        return "too short"
    return "ok"

# Apply it
print(title_quality("Acme Running Shoes — Free UK Delivery"))
```

The `def` keyword defines a function; arguments can have defaults; the type hints (`: str`, `-> str`) are optional but make code readable. This is how every shared SEO Colab script (Lee Foot's, Greg Bernhardt's, etc.) is structured.

## 9. Imports — `import pandas as pd`

A library is a package of pre-written code. **Two distinct steps**:

1. **`pip install pandas`** — downloads the library to your machine (do once per environment).
2. **`import pandas as pd`** — loads it into the *current script*, with `pd` as a short alias.

```python
import pandas as pd            # the alias 'pd' is universal convention
import requests                # no alias needed
from bs4 import BeautifulSoup  # import a single class from a library
import advertools as adv       # advertools' standard alias
```

If you `import` something you haven't `pip install`-ed, Python raises `ModuleNotFoundError`. That is one of the two errors you'll see most as a beginner; the fix is always `pip install <name>`.

## 10. Reading and writing files

```python
# Plain text
with open("urls.txt") as f:
    urls = [line.strip() for line in f]

# CSV via the standard library (rare in SEO; most use pandas)
import csv
with open("output.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["url", "status"])
    w.writerow(["/a", 200])

# CSV via pandas (the SEO default)
import pandas as pd
df = pd.read_csv("screaming_frog_internal_html.csv")
df.to_csv("clean.csv", index=False)

# Excel (Screaming Frog and many enterprise tools export .xlsx)
df = pd.read_excel("ahrefs_export.xlsx")
df.to_excel("output.xlsx", index=False)
```

The `with open(...) as f:` pattern is called a context manager — it auto-closes the file when the block exits, even if an error occurs.

## 11. Error handling — `try / except`

Real SEO scripts hit the network, the network fails, APIs rate-limit, URLs timeout. Without `try/except`, one bad URL kills your 50K-URL crawl on row 327. JC Chouinard's [exceptions tutorial](https://www.jcchouinard.com/python-exceptions/) lays it out:

```python
import requests

def fetch(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.status_code
    except requests.Timeout:
        return "TIMEOUT"
    except requests.ConnectionError:
        return "CONN_ERR"
    except requests.HTTPError as e:
        return f"HTTP_{e.response.status_code}"
    except Exception as e:
        return f"OTHER:{e}"
```

This pattern is non-negotiable in any production SEO script.

## 12. Working with APIs — REST, `requests.get()`, JSON

A **REST API** is an HTTP endpoint that returns structured data, almost always JSON. An SEO consultant interacts with at least: GSC, GA4, PageSpeed Insights, Ahrefs, SEMrush, DataForSEO, OpenAI.

The universal pattern with the `requests` library:

```python
import requests

PSI_KEY = "AIza..."   # your PageSpeed Insights API key
url     = "https://example.com"

resp = requests.get(
    "https://www.googleapis.com/pagespeedonline/v5/runPagespeed",
    params  = {"url": url, "key": PSI_KEY, "strategy": "mobile"},
    headers = {"User-Agent": "MyAuditScript/1.0"},
    timeout = 60,
)
data = resp.json()                 # parse JSON → dict
score = data["lighthouseResult"]["categories"]["performance"]["score"] * 100
print(f"{url}: {score}")
```

Three things to internalise:

- `params=` builds the query string (`?url=...&key=...`).
- `headers=` is where you set `User-Agent` (often required), `Authorization: Bearer ...` for OAuth tokens, or `Accept: application/json`.
- `resp.json()` only works if the response actually is JSON. Otherwise use `resp.text`.

## 13. String manipulation — f-strings, `.replace()`, `.lower()`, `.strip()`, `.split()`

Every scraped page comes back as messy strings. The cleanup vocabulary:

```python
title = "  Best  Running  Shoes  | Acme  \n"

clean = title.strip()                          # remove leading/trailing whitespace
lower = clean.lower()                          # "best  running  shoes  | acme"
no_brand = clean.replace(" | Acme", "")        # remove suffix
parts = clean.split("|")                       # ['Best  Running  Shoes  ', ' Acme  ']

# f-strings — string interpolation
keyword = "running shoes"
volume = 8400
print(f"{keyword}: {volume:,} searches")       # running shoes: 8,400 searches

# Slug generation, a classic SEO chore
import re
def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)       # drop punctuation
    text = re.sub(r"[\s_]+", "-", text)        # spaces → dashes
    return text.strip("-")

slugify("Best Running Shoes (2026)!")          # 'best-running-shoes-2026'
```

## 14. List comprehensions

A compact `for`-loop-into-a-list pattern. Once you read it, half of every SEO Colab snippet suddenly makes sense:

```python
urls = ["/a", "/b", "/c"]

# Without comprehension
abs_urls = []
for u in urls:
    abs_urls.append("https://example.com" + u)

# With comprehension — same result
abs_urls = ["https://example.com" + u for u in urls]

# With a filter
status = {"/a": 200, "/b": 404, "/c": 301}
broken = [u for u, s in status.items() if s == 404]   # ['/b']
```

Lee Foot's redirect-mapping script opens with exactly this pattern to read URL lists from text files: `[line.strip() for line in file]`.

## 15. `.py` files vs Jupyter notebooks `.ipynb`

| | `.py` file | Jupyter / Colab `.ipynb` |
|---|---|---|
| Format | Plain text | JSON containing cells |
| Run as | `python script.py` (top-to-bottom) | Cell-by-cell, in any order |
| Best for | Production, scheduled jobs, CLIs, version control with diffs | Exploratory analysis, tutorials, sharing visuals |
| Output | Stdout / files | Inline charts and dataframes alongside code |

**Rule of thumb:** start in a notebook to *figure out* the script, then once it's stable, copy it into a `.py` file for scheduling. JC Chouinard makes the same recommendation in his [introduction to running Python](https://www.jcchouinard.com/learn-python/).

---

# SECTION 2 — Python for SEO: Deep Practical Knowledge

## 2.1 Web Scraping

**What it solves.** You need title tags, H1s, canonicals, meta descriptions, schema, internal links, hreflang, prices, stock status — for either your own site or a competitor's — at a scale where Screaming Frog is overkill or where you want to integrate the result into a pipeline.

**API vs scrape.** If an API exists, use it. Scraping is for the long tail of pages that don't expose an API: competitor product pages, supplier catalogues, news sites, your own site when the dev team won't give you DB access.

### `requests` — the HTTP fetch

```python
import requests

HEADERS = {
    # Pretend to be a real browser. Many sites block default Python UA.
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"),
    "Accept-Language": "en-GB,en;q=0.9",
}

r = requests.get("https://example.com/", headers=HEADERS, timeout=15)
print(r.status_code, len(r.text))      # 200 1256
```

Key response attributes: `r.status_code`, `r.text` (HTML as string), `r.content` (bytes), `r.headers` (response HTTP headers — useful for `X-Robots-Tag`, `Content-Type`, `Last-Modified`), `r.url` (final URL after redirects), `r.history` (the redirect chain).

### `BeautifulSoup` — the HTML parser

`BeautifulSoup` (the `bs4` library) turns HTML into a navigable tree. Combined with `lxml` as the parsing backend, it handles the malformed HTML real websites ship.

```python
from bs4 import BeautifulSoup
import requests, json

r = requests.get("https://example.com/", headers=HEADERS, timeout=15)
soup = BeautifulSoup(r.text, "lxml")

title       = soup.find("title").get_text(strip=True)
h1          = soup.find("h1").get_text(strip=True) if soup.find("h1") else None
canonical   = (soup.find("link", rel="canonical") or {}).get("href")
meta_robots = (soup.find("meta", attrs={"name": "robots"}) or {}).get("content")
desc        = (soup.find("meta", attrs={"name": "description"}) or {}).get("content")

# All internal links
internal = [a["href"] for a in soup.find_all("a", href=True)
            if a["href"].startswith("/") or "example.com" in a["href"]]

# JSON-LD blocks (structured data)
ld_blocks = [json.loads(s.string) for s in soup.find_all(
    "script", type="application/ld+json") if s.string]
```

That single block is essentially a bulk title/H1/meta/canonical/schema checker — the foundation of 80% of "what's on these 10,000 pages" scripts.

### Pagination & politeness

```python
import time, random
for page in range(1, 51):
    r = requests.get(f"https://example.com/blog?page={page}", headers=HEADERS, timeout=15)
    if r.status_code != 200:
        break
    # ...parse...
    time.sleep(random.uniform(1.0, 2.5))   # be a polite citizen
```

Always `time.sleep` between requests. 1–2 seconds is a reasonable default for ad-hoc work. Honor `robots.txt` (see §2.9). Set a real `User-Agent` that identifies you, or at minimum a recognisable one.

### Don't scrape Google directly

Hammering `google.com/search` will get your IP banned within minutes and violates Google's ToS. Use a SERP API instead — **SerpApi**, **DataForSEO SERP API**, **ValueSERP**, **Bright Data SERP**, **Oxylabs SERP**. They handle the proxies, CAPTCHAs, and ToS exposure for you.

```python
# Example: DataForSEO SERP via requests
import requests
auth = ("login@email.com", "API_PASSWORD")
body = [{"language_code": "en", "location_code": 2826,        # UK
         "keyword": "running shoes", "device": "desktop"}]
r = requests.post("https://api.dataforseo.com/v3/serp/google/organic/live/regular",
                  auth=auth, json=body)
results = r.json()["tasks"][0]["result"][0]["items"]
```

### Realistic SEO scraping tasks

| Task | Selector pattern |
|---|---|
| Bulk title/H1/meta checker | `soup.find("title")`, `soup.find("h1")`, `soup.find("meta", attrs={"name":"description"})` |
| Internal link extractor | `soup.find_all("a", href=True)` filtered by domain |
| Hreflang map | `soup.find_all("link", rel="alternate", hreflang=True)` |
| JSON-LD extractor | `soup.find_all("script", type="application/ld+json")` |
| Competitor pricing | site-specific CSS selectors via `soup.select(".price")` |
| `<meta name="robots">` | `soup.find("meta", attrs={"name":"robots"})` |

### Scrapy vs requests + BS4

- **`requests` + BS4**: best for ≤ ~10K URLs, ad-hoc, in a notebook. Linear, easy to debug.
- **`Scrapy`**: a full crawling framework — async, middlewares, automatic deduping, pipelines, retry policies, throughput in the millions. Steeper learning curve. Use when you need to crawl whole sites at scale.

### The higher-level shortcut: `advertools.crawl()`

Elias Dabbas's `advertools` wraps Scrapy with sensible SEO defaults. One line crawls a site and dumps every important on-page element to a DataFrame:

```python
import advertools as adv
import pandas as pd

adv.crawl("https://example.com", output_file="crawl.jl", follow_links=True)
df = pd.read_json("crawl.jl", lines=True)
df[["url","title","h1","meta_desc","status","canonical"]].head()
```

`advertools` extracts titles, all heading levels, canonicals, meta robots, OG tags, JSON-LD, response/request headers, and lets you pass custom CSS/XPath selectors. For most consultants this replaces both Scrapy and a lot of Screaming Frog work. Reference: the [advertools docs](https://advertools.readthedocs.io/).

## 2.2 Data Manipulation with pandas

**Why pandas dominates SEO data work.** Every SEO data export — Screaming Frog crawl, Google Search Console export, Ahrefs backlink export, SEMrush keyword export, GA4 unsampled report — is a tabular CSV/Excel. pandas turns those into in-memory DataFrames you can filter, join, group and pivot in seconds.

### Reading and inspecting

```python
import pandas as pd

df = pd.read_csv("internal_html.csv")          # Screaming Frog export
gsc = pd.read_excel("gsc_pages.xlsx")          # GSC export
bl  = pd.read_csv("ahrefs_backlinks.csv")
js  = pd.read_json("crawl.jl", lines=True)     # advertools output

df.shape         # (rows, cols)
df.head()        # first 5 rows
df.info()        # dtypes + null counts per column
df.describe()    # numeric summary
df.columns       # column names
```

### Filtering — your `df[df['col'] == value]` muscle

```python
# All 404s
df[df["Status Code"] == 404]

# Pages with title length issues
df[(df["Title 1 Length"] > 60) | (df["Title 1 Length"] < 30)]

# Only blog URLs
df[df["Address"].str.contains("/blog/", na=False)]

# Pages that are 200 AND indexable AND have an H1
mask = (df["Status Code"] == 200) & (df["Indexability"] == "Indexable") & df["H1-1"].notna()
df[mask]
```

### Selecting & renaming

```python
df = df[["Address", "Title 1", "H1-1", "Status Code", "Word Count"]]
df = df.rename(columns={"Address": "url", "Title 1": "title", "H1-1": "h1",
                        "Status Code": "status", "Word Count": "wc"})
```

### Merging — the "VLOOKUP for Python"

This is the single most useful pandas skill for an SEO. You constantly want to glue *crawl + GSC + GA4 + backlinks* together on a URL key.

```python
# Crawl data + GSC clicks + GA4 sessions, all on URL
combined = (crawl_df
            .merge(gsc_df,  on="url", how="left")
            .merge(ga4_df,  on="url", how="left")
            .merge(bl_df,   on="url", how="left"))

combined.head()
```

`how="left"` keeps every row of the left DataFrame even if there's no match on the right (the equivalent of an Excel VLOOKUP returning N/A). Hamlet Batista's "[How To Use Python to Analyze SEO Data: A Reference Guide](https://www.searchenginejournal.com/python-seo-data-reference-guide/287927/)" treats this `pd.merge` as the keystone operation of SEO data science. Greg Bernhardt has a whole [SEO Data Blending with Python](https://importsem.com/seo-data-blending-with-python-for-beginners/) tutorial dedicated to it.

### `groupby` and aggregations

```python
# 404s per top-level folder
errors = df[df["status"] == 404].copy()
errors["folder"] = errors["url"].str.split("/").str[3]   # crude folder bucket
errors.groupby("folder").size().sort_values(ascending=False)

# Average word count by category
df.groupby("category")["wc"].mean().round(0)

# Multi-metric aggregation
df.groupby("category").agg(
    pages       = ("url", "count"),
    avg_wc      = ("wc",  "mean"),
    total_clicks= ("clicks","sum"),
)
```

### Cleaning & I/O

```python
df = df.drop_duplicates(subset=["url"])
df = df.sort_values("clicks", ascending=False).reset_index(drop=True)

df.to_csv("output.csv", index=False)
df.to_excel("output.xlsx", index=False)
df.to_parquet("output.parquet")              # 10–100× smaller than CSV
```

### Handling large files

For multi-million-row log files or full Ahrefs exports:

- **Chunking:** `for chunk in pd.read_csv("huge.csv", chunksize=200_000): ...`
- **Parquet:** binary columnar format, far faster to read/write and far smaller. Use `df.to_parquet()` once and never go back to CSV for big data. `advertools.logs_to_df()` natively writes parquet.
- **Polars / DuckDB:** if pandas runs out of RAM, pivot to one of these. Same DataFrame mental model, much faster.

### Real SEO use cases

- **Crawl analysis:** filter by status, by indexability, by depth, by template.
- **Duplicate detection:** `df[df.duplicated(subset=["title"], keep=False)]` finds duplicate titles; same on H1s.
- **Keyword cannibalisation:** group GSC data by query, count distinct pages, flag queries where >1 URL has impressions.
- **Content gap analysis:** anti-join Ahrefs competitor keywords with your own ranking keywords.
- **Striking-distance pages:** filter GSC to `position` between 11 and 20 with non-trivial impressions.

## 2.3 Automation

"Automation" in SEO means: scripts that run themselves on a schedule, batch-process whole folders of files, replace recurring manual chores, and connect tools that don't natively talk to each other.

### `os` and `pathlib`

```python
from pathlib import Path

# Process every CSV in an exports/ folder
for csv in Path("exports").glob("*.csv"):
    df = pd.read_csv(csv)
    print(csv.name, df.shape)
```

`pathlib` is the modern replacement for the older `os.path` API. Everything you used to do with string-concatenated paths becomes attribute access: `path.stem`, `path.suffix`, `path.parent`.

### `subprocess` — driving Screaming Frog from Python

Screaming Frog has a CLI. You can fire crawls headlessly and pull the results into pandas:

```python
import subprocess, pandas as pd

subprocess.run([
    "/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher",
    "--crawl", "https://example.com",
    "--headless",
    "--save-crawl",
    "--output-folder", "./sf_out",
    "--export-tabs", "Internal:HTML",
])
df = pd.read_csv("./sf_out/internal_html.csv")
```

Greg Bernhardt has a whole [Automating Screaming Frog with Python](https://importsem.com/) walkthrough on importSEM.

### Scheduling

| OS / target | Tool | Use |
|---|---|---|
| Mac/Linux | `cron` (`crontab -e`) | `0 7 * * 1 /path/.venv/bin/python /path/script.py` runs every Monday at 07:00 |
| Windows | Task Scheduler | GUI-driven equivalent |
| Cloud (free) | **GitHub Actions** | A `.github/workflows/seo.yml` file runs your script on a schedule against a hosted runner; perfect for weekly GSC dumps |
| Cloud (paid) | Google Cloud Scheduler + Cloud Run / Cloud Functions | For heavier jobs |

JC Chouinard's [crontab automation post](https://www.jcchouinard.com/) and Greg Bernhardt's [Google Cloud Functions tutorial](https://importsem.com/) cover both ends.

### `gspread` — read & write Google Sheets

[`gspread`](https://docs.gspread.org/) is the canonical wrapper for the Google Sheets API. The minimal pattern:

```python
import gspread
import pandas as pd

gc = gspread.service_account(filename="service_account.json")
sh = gc.open_by_key("1AbC...XYZ")          # the sheet ID from its URL
ws = sh.worksheet("GSC Weekly")

# Read into DataFrame
df = pd.DataFrame(ws.get_all_records())

# Write a DataFrame back
ws.clear()
ws.update([df.columns.tolist()] + df.values.tolist())
```

This is the backbone of every "weekly dashboard auto-updates from a script" workflow.

### `smtplib` — email automation

```python
import smtplib, ssl
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Weekly SEO alert: 14 new 404s detected"
msg["From"]    = "alerts@yourdomain.com"
msg["To"]      = "client@example.com"
msg.set_content("See attached.")
msg.add_attachment(open("404s.csv","rb").read(), maintype="text",
                   subtype="csv", filename="404s.csv")

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as s:
    s.login("alerts@yourdomain.com", "APP_PASSWORD")
    s.send_message(msg)
```

For Gmail use an App Password, not your normal password.

### Make / n8n vs Python

- **Make.com / n8n / Zapier**: best for stitching SaaS APIs together with no code. Limited when you need pandas-grade data manipulation, ML, or custom logic.
- **Python**: best when the heart of the workflow is *transforming* or *modelling* data, or when SaaS pricing makes per-operation billing too expensive.
- **Common pattern:** n8n triggers a Python script (via webhook or shell node), Python does the heavy work, n8n distributes the result.

### Real automation examples

1. **Weekly GSC dump → Google Sheet** (cron + `google-searchconsole` + `gspread`). Replaces manual exports forever.
2. **Daily redirect-chain checker** that emails you any time a 200→301→200 chain breaks.
3. **Scheduled crawl** that diffs against last week's crawl and alerts on new 404s, new noindexes, missing canonicals.
4. **PageSpeed Insights tracker** that logs LCP/CLS/INP for the top 100 URLs every Monday into BigQuery.

## 2.4 Google Search Console API

**Why the API matters.** The GSC UI tops out at 1,000 rows per query and ~16 months of history (and only 3 months of "recent" UI views in some screens). The API gives you up to **25,000 rows per request** (paginated to effectively unlimited) and the full **16 months** of data.

### Setup

1. Google Cloud Console → create a project.
2. Enable the **Search Console API**.
3. Credentials → **Create OAuth client ID** → Desktop application → download the `client_secrets.json`.
4. Verify the GSC property is owned by your Google account.

JC Chouinard's [Google Search Console API guide](https://www.jcchouinard.com/google-search-console-api/) has the screen-by-screen walkthrough.

### `google-searchconsole` (Josh Carty's wrapper)

This library makes GSC pleasant to query. From [the GitHub README](https://github.com/joshcarty/google-searchconsole):

```python
import searchconsole

account = searchconsole.authenticate(
    client_config="client_secrets.json",
    credentials="credentials.json",
)
webproperty = account["https://www.example.com/"]

report = (webproperty.query
          .range("today", days=-90)
          .dimension("page", "query")
          .limit(25000)
          .get())

df = report.to_dataframe()
```

Filter by device, country, search type:

```python
report = (webproperty.query
          .range("today", days=-90)
          .dimension("query")
          .filter("country", "gbr", "equals")
          .filter("device", "MOBILE", "equals")
          .filter("page", "/blog/", "contains")
          .get())
```

### Killer GSC use cases

- **Cannibalisation detection:** group by query, count distinct top-ranking URLs.
  ```python
  cannib = (df.groupby("query")
              .agg(pages=("page","nunique"), clicks=("clicks","sum"))
              .query("pages > 1 and clicks > 10")
              .sort_values("clicks", ascending=False))
  ```
- **Striking distance pages (positions 11–20):** prime CTR optimisation candidates.
  ```python
  striking = df[(df.position.between(11, 20)) & (df.impressions > 100)]
  ```
- **CTR anomaly detection:** flag queries where actual CTR is far below expected for that position.
- **Brand vs non-brand split:** `df["brand"] = df["query"].str.contains("acme", case=False)`.
- **Keyword tracking over time:** weekly snapshots into BigQuery or a Sheet.

### Visualising GSC data

```python
import plotly.express as px

fig = px.scatter(df, x="position", y="ctr", size="impressions",
                 hover_name="query", color="impressions",
                 title="GSC — CTR vs Position")
fig.show()
```

JC Chouinard has a full ["Visualize GSC with Python and Plotly"](https://www.jcchouinard.com/visualize-gsc-with-python-plotly-and-machine-learning/) walkthrough including bubble charts.

## 2.5 Log File Analysis

**Why logs matter.** Server logs (Apache `access.log`, Nginx `access.log`) record every single request your server received — including every Googlebot hit. They are the only ground-truth source for: **how often Google actually crawls each URL**, **which sections eat your crawl budget**, **which URLs Google has discovered but never crawled**, **whether your JS-rendered pages are being fetched twice**, and **how many fake Googlebots are hitting you**.

### What a Googlebot log line looks like

```
66.249.73.72 - - [16/Feb/2026:00:18:53 +0000] "GET / HTTP/1.1" 200 1095 "-"
"Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36
(KHTML, like Gecko) Chrome/124 Mobile Safari/537.36 (compatible; Googlebot/2.1;
+http://www.google.com/bot.html)"
```

Fields: IP, timestamp, request line, status, bytes, referrer, user-agent.

### Verifying real Googlebot — `dnspython`

User-agent strings are trivially spoofed. Google's [official guidance](https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot) is forward-confirmed reverse DNS: reverse the IP, check the hostname ends in `.googlebot.com` / `.google.com`, then forward-resolve and confirm the IPs match.

```python
from dns import resolver, reversename

def is_real_googlebot(ip: str) -> bool:
    try:
        rev = reversename.from_address(ip)
        host = str(resolver.resolve(rev, "PTR")[0]).rstrip(".")
        if not (host.endswith(".googlebot.com") or host.endswith(".google.com")):
            return False
        # Forward-resolve and confirm
        ips = [str(a) for a in resolver.resolve(host, "A")]
        return ip in ips
    except Exception:
        return False
```

`advertools` ships a vectorised version: `adv.reverse_dns_lookup(ip_list)` returns a DataFrame with hostname, alias list, counts and percentages — efficient because it dedupes the IPs first.

### `advertools.logs_to_df()` — the fastest approach

```python
import advertools as adv
import pandas as pd

adv.logs_to_df(
    log_file    = "access.log",
    output_file = "access.parquet",     # parquet is required
    errors_file = "errors.csv",         # malformed lines land here
    log_format  = "common",             # also: "combined", or pass a regex
)
df = pd.read_parquet("access.parquet")
df.head()
```

`advertools` knows the canonical log formats and produces a tidy DataFrame in one call. See [advertools log analysis docs](https://advertools.readthedocs.io/en/master/advertools.logs.html).

### Manual parsing with `re`

For non-standard log formats:

```python
import re
LOG_RE = re.compile(
  r'(?P<ip>\S+) \S+ \S+ \[(?P<ts>[^\]]+)\] '
  r'"(?P<method>\S+) (?P<path>\S+) [^"]+" '
  r'(?P<status>\d+) (?P<bytes>\S+) "[^"]*" "(?P<ua>[^"]+)"'
)
rows = [m.groupdict() for line in open("access.log") if (m := LOG_RE.match(line))]
df = pd.DataFrame(rows)
```

### Key metrics to extract

```python
gb = df[df["user_agent"].str.contains("Googlebot", na=False)]

# Crawl frequency by URL
gb.groupby("url").size().sort_values(ascending=False).head(20)

# Crawl budget by section
gb["section"] = gb["url"].str.split("/").str[1]
gb.groupby("section").size()

# Status distribution Google sees
gb["status"].value_counts(normalize=True) * 100

# Pages crawled but not in your sitemap
sitemap_urls = set(adv.sitemap_to_df("https://example.com/sitemap.xml")["loc"])
crawled_only = set(gb["url"]) - sitemap_urls
```

### Real use cases

- **Crawl budget diagnosis:** are 60% of Googlebot hits going to faceted filter URLs? Block them.
- **JS rendering validation:** does Googlebot fetch both your HTML and the underlying JS bundles? Two requests per page typically means rendering is happening.
- **Bot traffic audit:** what % of "Googlebot" hits failed reverse-DNS verification? (Often 20–40% — those are scrapers.)
- **First-crawl date per page:** join logs with publish date to measure indexation lag.

## 2.6 Redirect Mapping for Migrations

**The problem.** A migration moves 10,000 URLs from `/old/whatever/` to `/new/whatever-redesigned/`. Without a mapping table, every old URL becomes a 404 or a useless homepage redirect, and you lose the link equity. Manually mapping 10K URLs is a week of misery.

**The Python answer:** crawl old + new, fuzzy-match on slug / title / H1, auto-accept high-confidence matches, manually QA the rest.

### `polyfuzz` — the canonical library

[`polyfuzz`](https://github.com/MaartenGr/PolyFuzz) by Maarten Grootendorst supports TF-IDF, Levenshtein (edit distance), FastText/GloVe embeddings, and SentenceTransformer/BERT embeddings, all behind one API. The minimal pattern from Lee Foot's [`migration_mapper`](https://github.com/searchsolved/search-solved-public-seo/blob/main/migration_mapper/migration_mapper.py):

```python
from polyfuzz import PolyFuzz
import pandas as pd

old_df = pd.read_csv("internal_html_old.csv")
new_df = pd.read_csv("internal_html_new.csv")

old_urls = old_df["Address"].tolist()
new_urls = new_df["Address"].tolist()

model = PolyFuzz("TF-IDF").match(old_urls, new_urls)
matches = model.get_matches()      # DataFrame: From | To | Similarity
```

For better quality, match on titles or H1s rather than raw URLs:

```python
old_titles = old_df["Title 1"].tolist()
new_titles = new_df["Title 1"].tolist()

model = PolyFuzz("TF-IDF").match(old_titles, new_titles)
out = model.get_matches()
out = out.merge(old_df[["Title 1","Address"]], left_on="From", right_on="Title 1")
out = out.merge(new_df[["Title 1","Address"]], left_on="To",   right_on="Title 1")
out = out.rename(columns={"Address_x":"old_url","Address_y":"new_url"})
```

### `RapidFuzz` — faster Levenshtein-only

[`rapidfuzz`](https://github.com/maxbachmann/RapidFuzz) is a drop-in C++-backed replacement for `fuzzywuzzy`. Far faster, but Levenshtein-only — best when input is already normalised.

```python
from rapidfuzz import process, fuzz
process.extractOne("running shoes", choices=new_titles, scorer=fuzz.WRatio)
```

### Quality thresholds (Lee Foot's heuristic)

| Similarity | Action |
|---|---|
| ≥ 90% | Auto-accept |
| 70–90% | Human QA |
| < 70% | Manual mapping or send to homepage / parent category |

```python
matches["bucket"] = pd.cut(matches["Similarity"],
                           bins=[-0.01, 0.7, 0.9, 1.01],
                           labels=["manual","qa","auto"])
```

### Edge cases

- **Trailing slashes:** normalise both lists with `url.rstrip("/")` before matching.
- **Query parameters:** strip irrelevant params (`utm_*`) but keep meaningful ones (`?id=`).
- **URL encoding:** `urllib.parse.unquote(url)` decodes `%20` → space etc.
- **Pagination:** `?page=2`-style URLs should map to their unparameterised parents on most migrations.
- **Languages:** match within language buckets, not across them.

### When TF-IDF beats embeddings (and vice-versa)

- **TF-IDF**: fast, no GPU, excellent when slugs / titles share vocabulary. Lee Foot's default.
- **SentenceTransformer embeddings**: better when wording changed substantially during the migration ("Best Trail Running Shoes 2024" → "Top Outdoor Runners Buyer Guide").

## 2.7 Keyword Clustering & Semantic Analysis

**Why automate it.** A modern Ahrefs / SEMrush export is 10K–500K keywords. Manually grouping those into topical clusters for content briefs is impossible. Clustering at scale only works in code.

### Two families of approach

| Approach | Library | Speed | Quality | When |
|---|---|---|---|---|
| **TF-IDF + cosine similarity** | `scikit-learn` | Very fast, CPU only | Good for exact / phrase variants ("running shoes" / "running shoe") | Big lists, you mostly care about wording overlap |
| **Embedding-based** | `sentence-transformers` (free) or **OpenAI `text-embedding-3-small`** | Slower; GPU helps; embeddings $0.02 per 1M tokens via OpenAI | Captures *meaning* — "trainers for marathon training" clusters with "long-distance running shoes" | Topical clusters, intent grouping |

### Embedding-based with `sentence-transformers`

The model Lee Foot found best balance of speed/quality is `all-MiniLM-L6-v2` — a 384-dim model that's small (~80MB), fast, and surprisingly strong on short text:

```python
from sentence_transformers import SentenceTransformer
import numpy as np, pandas as pd

kws = pd.read_csv("keywords.csv")["Keyword"].tolist()

model = SentenceTransformer("all-MiniLM-L6-v2")
emb   = model.encode(kws, show_progress_bar=True, convert_to_numpy=True)
```

### Clustering algorithms

```python
# A) HDBSCAN — density-based, finds variable-size clusters, marks noise as -1
import hdbscan
hdb = hdbscan.HDBSCAN(min_cluster_size=5, metric="euclidean").fit(emb)
labels = hdb.labels_

# B) KMeans — you specify K
from sklearn.cluster import KMeans
km = KMeans(n_clusters=50, n_init="auto").fit(emb)

# C) Agglomerative with a similarity threshold
from sklearn.cluster import AgglomerativeClustering
ac = AgglomerativeClustering(distance_threshold=0.4, n_clusters=None,
                             metric="cosine", linkage="average").fit(emb)
```

| Algorithm | Pros | Cons |
|---|---|---|
| **HDBSCAN** | No need to set K. Naturally identifies "noise" keywords. Handles variable-density clusters. | Tuning `min_cluster_size`. Can leave many keywords unclustered. |
| **KMeans** | Fast, every point gets a cluster. | Must guess K; assumes globular clusters; pulls in unrelated outliers. |
| **Agglomerative (cosine + threshold)** | Intuitive: "cluster anything ≥ 85% similar." | O(n²) memory at large scale. |

Lee Foot's [SEJ semantic clustering Colab](https://colab.research.google.com/github/searchsolved/search-solved-public-seo/blob/main/search_engine_journal/SEJ_Semantic_Clustering_Tool_by_LeeFootSEO.ipynb) uses a community-detection-style approach on top of `all-MiniLM-L6-v2` and exposes a `cluster_accuracy` parameter (0–100). For 10K+ keywords with strong semantic clustering, this is the production reference.

### Embeddings via OpenAI

```python
from openai import OpenAI
client = OpenAI(api_key="sk-...")

resp = client.embeddings.create(model="text-embedding-3-small", input=kws[:100])
emb = np.array([d.embedding for d in resp.data])     # shape (100, 1536)
```

Released January 2024, `text-embedding-3-small` is **5× cheaper than `ada-002`**, multilingual, and supports the `dimensions` parameter to truncate to 256/512/etc. for storage savings. For SEO clustering you can usually shorten to 512 dimensions with negligible accuracy loss.

### `polyfuzz` for fuzzy dedup *before* clustering

Strip near-duplicates ("running shoes" / "running shoe") before clustering — it makes downstream clusters tighter:

```python
from polyfuzz import PolyFuzz
m = PolyFuzz("TF-IDF").match(kws, kws)
groups = m.group(link_min_similarity=0.92)  # collapses near-duplicates
```

### UMAP for visualisation

```python
import umap, plotly.express as px
xy = umap.UMAP(n_neighbors=15, min_dist=0.1).fit_transform(emb)
px.scatter(x=xy[:,0], y=xy[:,1], color=[str(l) for l in labels],
           hover_name=kws).show()
```

### Cannibalisation detection from GSC

Cluster every query in GSC, then for each cluster look at the URLs receiving impressions. If three URLs share clicks for one cluster, you have a cannibalisation problem.

### NLP basics — when you need them

- **Tokenisation** (split into words): `nltk.word_tokenize` or `spacy.lang.en.English`.
- **Stopwords**: NLTK ships English/Spanish/French/etc. stopword lists.
- **Stemming** (crude — chops endings): `PorterStemmer`. **Lemmatisation** (grammar-aware — "ran" → "run"): `spaCy`.
- **Named-entity recognition**: spaCy's `nlp(text).ents`. Greg Bernhardt has [a NER visualizer tutorial](https://importsem.com/build-a-custom-named-entity-visualizer-with-google-nlp/).

## 2.8 Reporting & Dashboard Automation

**The pattern.** Pull → Process → Push. Pull data from GSC + GA4 + crawl tools, process in pandas, push to a Google Sheet that Looker Studio reads. Refresh on schedule.

### GA4 Data API

The official Google library is `google-analytics-data`. JC Chouinard's [GA4 API tutorial](https://www.jcchouinard.com/google-analytics-api-using-python/):

```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (RunReportRequest,
                                                Dimension, Metric, DateRange)
import os, pandas as pd

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"
client = BetaAnalyticsDataClient()

req = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    date_ranges=[DateRange(start_date="28daysAgo", end_date="today")],
    dimensions=[Dimension(name="pagePath"), Dimension(name="sessionDefaultChannelGroup")],
    metrics=[Metric(name="sessions"), Metric(name="conversions")],
    limit=100_000,
)
resp = client.run_report(req)

rows = [[v.value for v in r.dimension_values] + [v.value for v in r.metric_values]
        for r in resp.rows]
cols = [d.name for d in resp.dimension_headers] + [m.name for m in resp.metric_headers]
ga4 = pd.DataFrame(rows, columns=cols)
```

### Looker Studio integration

Two production patterns:

1. **Sheet-as-source:** Python writes to Google Sheets via `gspread`; Looker Studio reads the Sheet. Free; trivial; up to ~50K rows comfortably.
2. **BigQuery-as-source:** Python writes to BigQuery via `google-cloud-bigquery`; Looker reads BigQuery. Production scale; faster refresh; costs cents per month at SEO data volumes.

### Combining GSC + GA4

```python
combined = (gsc.merge(ga4, left_on="page", right_on="pagePath", how="outer")
              .fillna(0))
combined["clicks_to_session_ratio"] = combined["clicks"] / combined["sessions"]
```

### Plotly for interactive charts

```python
import plotly.express as px
fig = px.scatter(gsc, x="impressions", y="ctr", size="clicks", color="position",
                 hover_name="query", log_x=True,
                 title="GSC bubble: impressions × CTR × position")
fig.write_html("dashboard.html")
```

A single HTML file you can email to a client. Plotly figures live-update in Jupyter and Colab too.

## 2.9 Technical SEO Automation

### Bulk status-code checker (with threading for speed)

```python
import requests
from concurrent.futures import ThreadPoolExecutor

def status(url):
    try:
        r = requests.head(url, allow_redirects=True, timeout=10,
                          headers={"User-Agent": "Mozilla/5.0"})
        return url, r.status_code, r.url
    except Exception as e:
        return url, "ERR", str(e)

with ThreadPoolExecutor(max_workers=20) as ex:
    rows = list(ex.map(status, urls))

df = pd.DataFrame(rows, columns=["url", "status", "final_url"])
```

`HEAD` is faster than `GET` because it skips the body. `ThreadPoolExecutor` parallelises I/O-bound work — 20 workers = ~20× speedup for network-bound checks.

### Bulk Core Web Vitals via PageSpeed Insights API

The PSI API (`/pagespeedonline/v5/runPagespeed`) returns both Lighthouse "lab" data and Chrome User Experience Report "field" data:

```python
import requests, os
KEY = os.environ["PSI_API_KEY"]

def psi(url, strategy="mobile"):
    r = requests.get(
        "https://www.googleapis.com/pagespeedonline/v5/runPagespeed",
        params={"url": url, "key": KEY, "strategy": strategy,
                "category": ["performance","accessibility","seo","best-practices"]},
        timeout=120)
    d = r.json()
    audits = d["lighthouseResult"]["audits"]
    crux   = d.get("loadingExperience", {}).get("metrics", {})
    return {
        "url": url,
        "perf": d["lighthouseResult"]["categories"]["performance"]["score"]*100,
        "lcp_ms": audits["largest-contentful-paint"]["numericValue"],
        "cls":    audits["cumulative-layout-shift"]["numericValue"],
        "tbt_ms": audits["total-blocking-time"]["numericValue"],
        "field_lcp": crux.get("LARGEST_CONTENTFUL_PAINT_MS", {}).get("category"),
    }
```

The PSI API has a 25,000/day, ~240/min quota. Use `aiohttp` for true async if you need more throughput; sleep 250ms between calls otherwise. Daniel Heredia and Ruth Everett both have full bulk-PSI tutorials online.

### XML sitemap parser — `advertools.sitemap_to_df()`

```python
import advertools as adv
sm = adv.sitemap_to_df("https://example.com/robots.txt")  # auto-discovers all sub-sitemaps
sm.head()      # columns: loc, lastmod, sitemap, etag, …
```

Now you can find:

```python
# noindex pages that still appear in the sitemap
crawl = pd.read_json("crawl.jl", lines=True)
junk  = crawl[crawl["meta_robots"].str.contains("noindex", na=False)]
in_sitemap_but_noindex = sm.merge(junk, left_on="loc", right_on="url")

# Stale URLs (lastmod > 12 months ago)
stale = sm[sm["lastmod"] < pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=365)]
```

### robots.txt — `advertools` and `urllib.robotparser`

```python
import advertools as adv
robots = adv.robotstxt_to_df("https://example.com/robots.txt")
# DataFrame with directive | content | robotstxt_url

# Bulk test which URLs are blocked for which user-agents
report = adv.robotstxt_test(
    "https://example.com/robots.txt",
    user_agents=["Googlebot", "Bingbot", "*"],
    urls=sm["loc"].tolist())
report[~report["can_fetch"]]   # rows where the URL is blocked
```

For lighter use, the standard library: `from urllib import robotparser`.

### Canonical, hreflang, schema validation

All three are one-pass tasks once you've crawled with `advertools` (which extracts canonicals, hreflang, and JSON-LD by default):

```python
crawl = pd.read_json("crawl.jl", lines=True)

# Self-referencing canonical check
crawl["self_canonical"] = crawl["canonical"] == crawl["url"]
crawl[~crawl["self_canonical"]]    # all canonical mismatches

# JSON-LD validity
import json
def parse_ld(s):
    try: return json.loads(s)
    except: return None
crawl["jsonld_parsed"] = crawl["jsonld"].apply(parse_ld)
```

For hreflang reciprocity (every page that points to /fr must be pointed to by /fr), build a directed graph from the hreflang pairs and find unmatched edges.

## 2.10 AI / LLM Integration (GEO bonus)

LLMs unlock three categories of SEO work that were impractical at scale: **content generation with guardrails**, **classification at scale**, and **brand citation monitoring (GEO)**.

### OpenAI API — embeddings + chat

```python
from openai import OpenAI
client = OpenAI(api_key="sk-...")

# Embeddings (2.7)
emb = client.embeddings.create(model="text-embedding-3-small",
                               input=["query A", "query B"]).data

# Chat completion — meta description generation
def gen_meta(title, h1, body_excerpt):
    msg = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"Write SEO meta descriptions, 140-155 chars, "
                                       "include a CTA, never invent facts."},
            {"role":"user","content":f"Title: {title}\nH1: {h1}\nExcerpt: {body_excerpt}"}
        ],
        temperature=0.4, max_tokens=80,
    )
    return msg.choices[0].message.content.strip()
```

### Anthropic / Claude — same pattern

```python
from anthropic import Anthropic
client = Anthropic()
resp = client.messages.create(model="claude-3-5-sonnet-latest", max_tokens=80,
    messages=[{"role":"user","content":"Write a 150-char meta description for..."}])
print(resp.content[0].text)
```

### The deterministic-first guardrail pattern

Don't spray LLM tokens at problems Python solves cheaply. Filter first; LLM only the residue.

```python
def needs_llm(row):
    if row["status"] != 200: return False           # not live, skip
    if pd.notna(row["meta_desc"]) and 140 <= len(row["meta_desc"]) <= 160:
        return False                                # already fine
    return True

todo = crawl[crawl.apply(needs_llm, axis=1)]
todo["new_meta"] = todo.apply(lambda r: gen_meta(r["title"], r["h1"], r["body"][:500]),
                              axis=1)
```

Hamlet Batista's last SEJ columns evangelised exactly this pattern: deterministic Python tier first, LLM tier second, human review tier third.

### Bulk meta description generator with hard guardrails

```python
def safe_meta(title, h1, body):
    out = gen_meta(title, h1, body)
    out = out.replace("\n", " ").strip().strip('"')
    if len(out) > 160:
        out = out[:157].rsplit(" ", 1)[0] + "…"
    if len(out) < 110:
        return None        # too short → flag for human
    return out
```

### Intent classification at scale

```python
LABELS = ["informational", "navigational", "transactional", "commercial"]
def classify_intent(query):
    msg = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system",
                   "content":f"Classify search intent into exactly one of {LABELS}."},
                  {"role":"user","content": query}],
        temperature=0, max_tokens=5)
    return msg.choices[0].message.content.strip().lower()
```

For large keyword sets it is far cheaper to (a) embed every query with `text-embedding-3-small`, (b) embed the four label descriptions, (c) assign each query to its nearest label by cosine similarity. That's $0.10 for 100K keywords vs $20 calling chat.

### GEO monitoring — tracking brand citations in LLM answers

Generative Engine Optimisation is the new frontier. Practical approaches:

1. **Perplexity API** — `pplx-7b-online` and `sonar` models hit the live web and return cited URLs. Query a list of category prompts daily; parse the citation list; track your domain's share.

   ```python
   import requests
   r = requests.post("https://api.perplexity.ai/chat/completions",
       headers={"Authorization": f"Bearer {PPLX_KEY}"},
       json={"model":"sonar","messages":[{"role":"user","content":"best running shoes"}],
             "return_citations": True})
   data = r.json()
   citations = data["citations"]              # list of cited URLs
   ```

2. **OpenAI web search tool** (via the Responses API) — similarly returns sources.

3. **DataForSEO LLM Mentions API** — indexes 200M+ AI responses across ChatGPT, Perplexity, Gemini, Claude; you query for your domain or brand and get mention/citation counts.

4. **Apify GEO actors** — pre-built scrapers that hit each LLM's public interface and emit structured "did your brand appear in answer to prompt X" datasets. Useful when official APIs don't expose what you need.

The pattern in all four: a list of category-defining prompts → query each LLM/API → record (prompt, answer, was-our-brand-mentioned, was-our-domain-cited, position) → aggregate weekly into share-of-voice and citation-rate KPIs.

---

# SECTION 3 — Key Libraries Summary Table

| Library | What it does | SEO use case | Difficulty | Install | Reference |
|---|---|---|---|---|---|
| **`requests`** | HTTP client | Hit any URL or REST API | ★ | `pip install requests` | [requests docs](https://requests.readthedocs.io) |
| **`beautifulsoup4`** | HTML parser | Extract titles, H1s, meta, schema | ★ | `pip install beautifulsoup4 lxml` | [Real Python BS4 guide](https://realpython.com/beautiful-soup-web-scraper-python/) |
| **`pandas`** | DataFrames | Crawl analysis, GSC, joins, filtering | ★★ | `pip install pandas` | [pandas docs](https://pandas.pydata.org/docs/) |
| **`advertools`** | All-in-one SEO toolkit | Crawl, sitemap_to_df, robotstxt_to_df, logs_to_df, reverse_dns_lookup, SERP | ★★ | `pip install advertools` | [advertools docs](https://advertools.readthedocs.io) |
| **`google-searchconsole`** | GSC API wrapper (Josh Carty) | 25K-row queries, 16 mo of data | ★★ | `pip install google-searchconsole` | [GitHub](https://github.com/joshcarty/google-searchconsole) |
| **`google-analytics-data`** | Official GA4 client | Sessions, conversions, landing pages | ★★ | `pip install google-analytics-data` | [GA4 API docs](https://developers.google.com/analytics/devguides/reporting/data/v1) |
| **`polyfuzz`** | Fuzzy string matching | Redirect mapping, dedup keywords | ★★ | `pip install polyfuzz` | [GitHub](https://github.com/MaartenGr/PolyFuzz) |
| **`rapidfuzz`** | Fast Levenshtein | Quick fuzzy matches without TF-IDF setup | ★ | `pip install rapidfuzz` | [GitHub](https://github.com/maxbachmann/RapidFuzz) |
| **`sentence-transformers`** | Embeddings (BERT family) | Semantic clustering, content matching | ★★★ | `pip install sentence-transformers` | [SBERT docs](https://www.sbert.net) |
| **`scikit-learn`** | Classical ML | KMeans, HDBSCAN, TF-IDF, classification | ★★★ | `pip install scikit-learn` | [scikit-learn docs](https://scikit-learn.org) |
| **`hdbscan`** | Density clustering | Cluster keyword embeddings | ★★ | `pip install hdbscan` | [docs](https://hdbscan.readthedocs.io) |
| **`umap-learn`** | Dimensionality reduction | Visualise keyword clusters | ★★ | `pip install umap-learn` | [docs](https://umap-learn.readthedocs.io) |
| **`nltk`** | Classical NLP | Stopwords, tokenising, stemming | ★★ | `pip install nltk` | [docs](https://www.nltk.org) |
| **`spaCy`** | Industrial NLP | Lemmatisation, NER, parsing | ★★ | `pip install spacy && python -m spacy download en_core_web_sm` | [docs](https://spacy.io) |
| **`plotly`** | Interactive charts | GSC bubbles, dashboards, share-of-voice | ★★ | `pip install plotly` | [docs](https://plotly.com/python/) |
| **`matplotlib`** | Static charts | Quick plots, publication graphics | ★★ | `pip install matplotlib` | [docs](https://matplotlib.org) |
| **`gspread`** | Google Sheets API | Read/write Sheets from Python | ★★ | `pip install gspread` | [gspread docs](https://docs.gspread.org) |
| **`python-dotenv`** | Load `.env` files | Keep API keys out of code | ★ | `pip install python-dotenv` | [GitHub](https://github.com/theskumar/python-dotenv) |
| **`tqdm`** | Progress bars | See a 50K-URL crawl progress | ★ | `pip install tqdm` | [GitHub](https://github.com/tqdm/tqdm) |
| **`Scrapy`** | Crawling framework | Production-scale crawls, pipelines | ★★★★ | `pip install scrapy` | [Scrapy docs](https://docs.scrapy.org) |
| **`dnspython`** | DNS lookups | Verify Googlebot via reverse DNS | ★★ | `pip install dnspython` | [docs](https://www.dnspython.org) |
| **`lxml`** | XML/HTML parser | Used as BS4 backend; XPath | ★★ | `pip install lxml` | [docs](https://lxml.de) |
| **`openpyxl`** | Excel I/O | Read/write `.xlsx` | ★ | `pip install openpyxl` | [docs](https://openpyxl.readthedocs.io) |
| **`openai`** | OpenAI API client | Embeddings, GPT, web search | ★★ | `pip install openai` | [platform.openai.com](https://platform.openai.com/docs) |
| **`anthropic`** | Anthropic API client | Claude completions | ★★ | `pip install anthropic` | [docs.anthropic.com](https://docs.anthropic.com) |

---

# SECTION 4 — Learning Roadmap (8 weeks)

A realistic week-by-week plan for the working SEO consultant who can spend ~5 hours/week on this. Each week has a *concrete deliverable* — by the end of week 8 you will have a portfolio of seven scripts running on real client data.

### Week 1–2: Python absolute basics

**Goal:** be able to write a 30-line script in Colab that reads a CSV, filters it, and writes the result.

- Open Google Colab. Read JC Chouinard's "[Learn Python](https://www.jcchouinard.com/learn-python/)" and "[3 Ways to Run Python](https://www.jcchouinard.com/)" tutorials — Colab, Jupyter, Spyder.
- Cover: `print`, variables, `str/int/float/bool`, lists, dicts, `for`, `while`, `if/elif/else`, functions, `import`, list comprehensions.
- **Deliverable:** Take a Screaming Frog `internal_html.csv`. Read it with `pd.read_csv`. Print the count of 404s. Write only the 404 rows to `404s.csv`.
- **Resources:** [Real Python beginners path](https://realpython.com/learning-paths/python-basics/), [Hamlet Batista's *Practical Introduction to Python for SEO Pros*](https://www.searchenginejournal.com/introduction-to-python-seo-spreadsheets/342779/) on SEJ, [freeCodeCamp's Python for Everybody](https://www.freecodecamp.org/learn/scientific-computing-with-python/), [Python.org tutorial](https://docs.python.org/3/tutorial/).

### Week 3: pandas on real SEO data

**Goal:** comfortably manipulate, filter, group, and merge SEO datasets.

- Read JC Chouinard's [Python Libraries for SEO](https://www.jcchouinard.com/python-libraries-for-seo/) (NumPy/pandas/matplotlib).
- Read Hamlet Batista's [How To Use Python to Analyze SEO Data: A Reference Guide](https://www.searchenginejournal.com/python-seo-data-reference-guide/287927/) on SEJ.
- Cover: read_csv/excel/json, head/info/describe, boolean filtering, `merge` (the VLOOKUP equivalent), `groupby`, `sort_values`, `drop_duplicates`, `to_csv`/`to_excel`.
- **Deliverable:** Merge a Screaming Frog crawl with a 90-day GSC export by URL. Output the top 50 pages with impressions but no clicks (CTR opportunity report).
- **Resources:** Greg Bernhardt's [SEO Data Blending with Python](https://importsem.com/seo-data-blending-with-python-for-beginners/), [Real Python pandas tutorials](https://realpython.com/learning-paths/pandas-data-science/).

### Week 4: requests + BeautifulSoup scraping

**Goal:** scrape your own and competitor pages at scale.

- Read JC Chouinard's [Web Scraping with BeautifulSoup](https://www.jcchouinard.com/web-scraping-with-beautifulsoup-in-python/).
- Read [Real Python's BS4 walkthrough](https://realpython.com/beautiful-soup-web-scraper-python/).
- Cover: `requests.get` with headers, `BeautifulSoup(html, "lxml")`, `.find` / `.find_all` / `.select`, attribute access, `time.sleep`, `try/except` for network errors.
- **Deliverable:** Bulk title/H1/meta/canonical/JSON-LD checker that takes a list of URLs and outputs a DataFrame.
- **Resources:** [`advertools.crawl()` docs](https://advertools.readthedocs.io/en/master/advertools.spider.html) as the higher-level shortcut.

### Week 5: Google Search Console API

**Goal:** programmatic GSC at >1K rows.

- Read JC Chouinard's [GSC API: Complete Guide (4 Chapters)](https://www.jcchouinard.com/google-search-console-api/).
- Set up OAuth credentials in Google Cloud Console.
- Install `google-searchconsole` (Josh Carty's wrapper).
- **Deliverable:** Pull 16 months of query/page data; build a striking-distance report (positions 11–20 with >100 impressions); detect cannibalisation (queries with multiple ranking URLs).
- **Resources:** [`joshcarty/google-searchconsole` GitHub](https://github.com/joshcarty/google-searchconsole), [JC Chouinard's wrapper-specific tutorial](https://www.jcchouinard.com/searchconsole-api-wrapper-python/).

### Week 6: Redirect mapping for migrations

**Goal:** auto-map 10K old URLs to 10K new URLs at >85% accuracy.

- Read Lee Foot's [`migration_mapper`](https://github.com/searchsolved/search-solved-public-seo/blob/main/migration_mapper/migration_mapper.py) on GitHub.
- Read Greg Bernhardt's [Generate a 404 Redirect List with PolyFuzz](https://importsem.com/generate-a-404-redirect-list-for-seo-with-polyfuzz-using-python/).
- Cover: `polyfuzz` TF-IDF and SentenceTransformer modes, similarity thresholds, edge cases (trailing slashes, query params).
- **Deliverable:** Take an old + new Screaming Frog crawl and output a `redirects.csv` with `from, to, similarity, bucket` columns.

### Week 7: advertools — crawl, sitemap, logs

**Goal:** master the all-in-one library that replaces a lot of manual technical-SEO work.

- Read Elias Dabbas's [advertools README](https://github.com/eliasdabbas/advertools) and the [adver.tools blog](https://blog.adver.tools/).
- Read Koray Tuğberk Gübür's [content analysis with sitemaps via Python](https://www.oncrawl.com/technical-seo/using-python-and-sitemaps-to-audit-content-strategies/) on OnCrawl.
- Cover: `adv.crawl()`, `adv.sitemap_to_df()`, `adv.robotstxt_to_df()`, `adv.robotstxt_test()`, `adv.logs_to_df()`, `adv.reverse_dns_lookup()`.
- **Deliverable:** Three scripts: (1) full sitemap audit (status, lastmod freshness, robots blocking), (2) 30-day Googlebot crawl analysis from server logs, (3) crawl + sitemap + log triangulation.

### Week 8: Keyword clustering — semantic + TF-IDF

**Goal:** cluster a 50K-keyword export into topical groups that map to content briefs.

- Read Lee Foot's [Semantic Keyword Clustering for 10,000+ Keywords](https://www.searchenginejournal.com/semantic-keyword-clustering-python/437166/) on SEJ. Open the Colab.
- Cover: `sentence-transformers` (`all-MiniLM-L6-v2`), TF-IDF clustering with `scikit-learn`, HDBSCAN vs KMeans vs Agglomerative, UMAP visualisation.
- **Deliverable:** Take an Ahrefs/SEMrush keyword export. Cluster semantically. Identify the 20 highest-volume clusters with no ranking content on your domain → that's your content roadmap for next quarter.
- **Bonus:** swap the local model for OpenAI `text-embedding-3-small` and compare results.

### Where to go next (months 3+)

- **Andreas Voniatis — *Data-Driven SEO with Python*** (Apress, 2023). The most comprehensive single book; covers ML, NLP, forecasting, and migrations applied to SEO.
- **Elias Dabbas's Maven course** "Data Science with Python for SEO" — hands-on with the advertools maintainer.
- **Hamlet Batista's complete SEJ archive** — irreplaceable. Title-tag deep learning, intent classification, crawler-trap detection, sitemap reorganisation, image alt-text generation. Linked from his [SEJ author page](https://www.searchenginejournal.com/author/hamlet-batista/).
- **Greg Bernhardt's [importSEM](https://importsem.com)** — 200+ tutorials, especially strong on automation and API integration.
- **JC Chouinard's full [Python for SEO course](https://www.jcchouinard.com/python-for-seo/)** — beginner to expert across 9 chapters; the most structured single resource online.
- **SearchPilot's blog** for SEO testing methodology, Will Critchlow's split-testing framework, and how to apply Python to A/B test analysis.
- **The advertools blog** (`blog.adver.tools`) for current production patterns from Elias Dabbas.

---

# Caveats

- **The Python and SEO library landscape moves fast.** Check the install command and minimum Python version in each library's current docs before adopting in production. `polyfuzz` in particular has had `sparse_dot_topn` install issues on some platforms. `sentence-transformers` versions matter for backward compatibility with downloaded models.
- **API surfaces change.** GA4's Data API is stable but its dimension/metric names differ from GA3. The GSC API has hard quotas (1,200 QPM, 1,200 QPD per user) and 25,000-rows-per-request caps. The PSI API limits to 25K/day, ~240/min. OpenAI's pricing and model snapshots evolve regularly — re-check before scaling a job.
- **Hamlet Batista passed away in January 2021.** His SEJ and Search Engine Land columns remain online and fundamental, but some specific code references libraries (e.g. older HuggingFace pipelines, older OpenAI completion endpoints) that have since been deprecated. The patterns are timeless; specific imports may need updating. The community-led [seopythonistas.com](https://seopythonistas.com), founded by Charly Wargnier, preserves and continues his work.
- **GEO monitoring tooling is nascent.** APIs from Perplexity, OpenAI, Anthropic and DataForSEO change rapidly; the Apify "AI brand monitor" actors mentioned in §2.10 are third-party scrapers whose stability varies. Treat any GEO-monitoring implementation as a 3-month rolling rebuild, not a build-and-forget asset.
- **Don't scrape Google directly.** Repeated mention deserves repeating: scraping `google.com/search` violates Google's Terms of Service, will get your IP blocked, and produces unreliable data anyway. Use SerpApi, DataForSEO SERP, ValueSERP, Bright Data, or Oxylabs.
- **Validate Googlebot.** A meaningful share of traffic claiming to be Googlebot is not. Forward-confirmed reverse DNS (or `advertools.reverse_dns_lookup`) is the only reliable verification — user-agent strings alone are worthless for log analysis conclusions.
- **Code shown is illustrative.** Snippets in this guide are minimal patterns to convey the shape of working code, not production-hardened scripts. Add error handling, logging, retries, and credential management before running anything against client data.
- **Difficulty ratings in the libraries table are subjective** and assume the reader has completed at least Section 1 of this guide; raw beginners will find pandas harder than ★★, and an experienced developer will find Scrapy easier than ★★★★.