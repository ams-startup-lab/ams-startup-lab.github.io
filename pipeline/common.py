"""Shared helpers for the pipeline scripts. Standard library plus PyYAML only."""
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "pipeline" / "out"
# OpenAlex and Crossref ask for a contact address in the User-Agent ("polite pool").
USER_AGENT = "ams-startup-lab-site/1.0 (+https://www.ams-startup-lab.org)"
# Fallback when no API credential is configured on the environment.
API_KEY_ENV_NAME = "OPENALEX_API_KEY"


def load_yaml_dir(name):
    """Return {slug: dict} for every YAML file in data/<name>/."""
    items = {}
    for path in sorted((DATA / name).glob("*.yaml")):
        items[path.stem] = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return items


def load_rejected():
    path = DATA / "rejected.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}
    raw = raw or {}
    return {
        "dois": {norm_doi(d) for d in raw.get("dois") or []},
        "urls": {norm_url(u) for u in raw.get("urls") or []},
    }


def norm_doi(doi):
    if not doi:
        return None
    doi = doi.strip().lower()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
    return doi or None


def norm_url(url):
    if not url:
        return None
    url = url.strip().split("#")[0]
    url = re.sub(r"[?&](utm_[^=]+|fbclid|gclid)=[^&]*", "", url)
    return url.rstrip("/?&").lower()


def norm_title(title):
    return re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()


def apa_pages(page=None, article_number=None):
    """Pages in APA 7 form: a range with an en dash ("1269–1289"), or "Article N"
    for journals that number articles. Returns None when there is nothing to show."""
    page = str(page or "").strip()
    if re.search(r"\d\s*[-‐‑–—]\s*\d", page):
        return re.sub(r"\s*[-‐‑–—]\s*", "–", page)
    if article_number:
        return f"Article {str(article_number).strip()}"
    return page or None


def fetch(url, timeout=30, retries=3):
    """GET a URL. Returns (status, final_url, text). Never raises on HTTP errors."""
    last = (0, url, "")
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read(3_000_000).decode("utf-8", errors="replace")
                return resp.status, resp.geturl(), body
        except urllib.error.HTTPError as err:
            last = (err.code, url, "")
            if err.code not in (429, 500, 502, 503, 504):
                return last
        except (urllib.error.URLError, TimeoutError, OSError) as err:
            last = (0, url, str(err))
        time.sleep(2 * (attempt + 1))
    return last


def fetch_json(url):
    status, _, body = fetch(url)
    if status != 200:
        return None
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return None


def write_out(name, payload):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}", file=sys.stderr)
    return path
