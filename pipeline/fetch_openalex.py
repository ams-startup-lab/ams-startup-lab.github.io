"""Find candidate publications for lab members on OpenAlex.

Deterministic: no judgement here. The routine (Claude) scores relevance later,
and the lab director approves each paper by merging its pull request.

Usage: python pipeline/fetch_openalex.py [--since YYYY-MM-DD]
Output: pipeline/out/publication_candidates.json
"""
import argparse
import datetime as dt
import os
import sys
import urllib.parse

from common import (API_KEY_ENV_NAME, fetch_json, load_rejected, load_yaml_dir,
                    norm_doi, norm_title, norm_url, write_out)

API = "https://api.openalex.org/works"
FIELDS = ",".join([
    "id", "doi", "title", "publication_year", "publication_date", "type",
    "authorships", "primary_location", "biblio", "topics",
    "abstract_inverted_index",
])
# OpenAlex gives anonymous callers almost no daily budget. A free API key lifts that.
# The key lives in the environment variable OPENALEX_API_KEY, never in this repository.
API_KEY = os.environ.get(API_KEY_ENV_NAME, "").strip()
DEFAULT_LOOKBACK_DAYS = 400  # indexing lags publication; rejected and approved papers are filtered out


def abstract_text(inverted, limit=900):
    if not inverted:
        return None
    words = sorted((pos, word) for word, poss in inverted.items() for pos in poss)
    return " ".join(w for _, w in words)[:limit]


def works_for(member, since):
    """Query by ORCID first, then by pinned OpenAlex author IDs."""
    filters = []
    if member.get("orcid"):
        filters.append(f"author.orcid:{member['orcid']}")
    if member.get("openalex_ids"):
        filters.append("author.id:" + "|".join(member["openalex_ids"]))
    found, ok = {}, bool(filters)
    for author_filter in filters:
        params = {
            "filter": f"{author_filter},from_publication_date:{since}",
            "select": FIELDS,
            "per-page": 100,
            "sort": "publication_date:desc",
        }
        if API_KEY:
            params["api_key"] = API_KEY
        query = urllib.parse.urlencode(params)
        payload = fetch_json(f"{API}?{query}")
        if payload is None:
            ok = False
            continue
        for work in payload.get("results", []):
            found[work["id"]] = work
    return list(found.values()), ok


def to_candidate(work):
    source = ((work.get("primary_location") or {}).get("source") or {})
    biblio = work.get("biblio") or {}
    pages = None
    if biblio.get("first_page"):
        pages = biblio["first_page"]
        if biblio.get("last_page") and biblio["last_page"] != biblio["first_page"]:
            pages += f"-{biblio['last_page']}"
    return {
        "openalex_id": work["id"],
        "doi": norm_doi(work.get("doi")),
        "title": work.get("title"),
        "authors": [a["author"]["display_name"] for a in work.get("authorships", [])],
        "year": work.get("publication_year"),
        "publication_date": work.get("publication_date"),
        "type": work.get("type"),
        "journal": source.get("display_name"),
        "is_preprint": source.get("type") == "repository" or work.get("type") == "preprint",
        "volume": biblio.get("volume"),
        "issue": biblio.get("issue"),
        "pages": pages,
        "url": work.get("doi") or (work.get("primary_location") or {}).get("landing_page_url"),
        "topics": [t["display_name"] for t in (work.get("topics") or [])[:3]],
        "abstract": abstract_text(work.get("abstract_inverted_index")),
        "members": [],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", help="YYYY-MM-DD; default is 400 days ago")
    args = parser.parse_args()
    today = dt.date.today()
    default_since = today - dt.timedelta(days=DEFAULT_LOOKBACK_DAYS)
    since_arg = dt.date.fromisoformat(args.since) if args.since else default_since

    members = load_yaml_dir("members")
    published = load_yaml_dir("publications")
    rejected = load_rejected()
    known_dois = {norm_doi(p.get("doi")) for p in published.values()} - {None}
    known_titles = {norm_title(p.get("title")) for p in published.values()}

    candidates, problems, skipped = {}, [], []
    for slug, member in members.items():
        if member.get("left"):
            continue
        if not member.get("orcid") and not member.get("openalex_ids"):
            skipped.append(slug)
            continue
        joined = member.get("joined")
        since = max(since_arg, joined) if joined else since_arg
        works, ok = works_for(member, since.isoformat())
        if not ok:
            problems.append(f"OpenAlex query failed for {slug}; run pipeline/openalex_status.py to see why")
        for work in works:
            cand = to_candidate(work)
            key = cand["doi"] or norm_title(cand["title"])
            if not key or not cand["title"]:
                continue
            if cand["doi"] in known_dois or norm_title(cand["title"]) in known_titles:
                continue
            if cand["doi"] in rejected["dois"] or norm_url(cand["url"]) in rejected["urls"]:
                continue
            candidates.setdefault(key, cand)["members"].append(slug)

    # Collapse a preprint and its published version (same title): keep the published one.
    by_title = {}
    for key, cand in candidates.items():
        title = norm_title(cand["title"])
        other = by_title.get(title)
        if other is None or (other["is_preprint"] and not cand["is_preprint"]):
            by_title[title] = cand
    result = sorted(by_title.values(), key=lambda c: c["publication_date"] or "", reverse=True)

    write_out("publication_candidates.json", {
        "generated": today.isoformat(),
        "since": since_arg.isoformat(),
        "members_without_ids": skipped,
        "problems": problems,
        "candidates": result,
    })
    print(f"{len(result)} candidates, {len(skipped)} members without IDs, {len(problems)} problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())
