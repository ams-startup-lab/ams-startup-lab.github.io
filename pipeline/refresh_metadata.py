"""Propose low-risk metadata completions for publications already on the site.

For each publication with a DOI that lacks volume, issue, or pages (or is
marked in_press), ask Crossref for the current record. Only these fields may
change through the auto path: status, volume, issue, pages, year.

Usage: python pipeline/refresh_metadata.py
Output: pipeline/out/metadata_updates.json
"""
import sys
import urllib.parse

from common import fetch_json, load_yaml_dir, write_out


def main():
    updates, problems = [], []
    for slug, pub in load_yaml_dir("publications").items():
        doi = pub.get("doi")
        complete = pub.get("volume") and pub.get("pages") and pub.get("status", "published") == "published"
        if not doi or complete:
            continue
        payload = fetch_json("https://api.crossref.org/works/" + urllib.parse.quote(doi))
        if payload is None:
            problems.append(f"Crossref lookup failed for {slug}")
            continue
        record = payload.get("message", {})
        changes = {}
        for field, key in (("volume", "volume"), ("issue", "issue"), ("pages", "page")):
            value = record.get(key)
            if value and str(value) != str(pub.get(field) or ""):
                changes[field] = str(value)
        if record.get("volume") and pub.get("status") == "in_press":
            changes["status"] = "published"
            year = ((record.get("published-print") or record.get("published") or {}).get("date-parts") or [[None]])[0][0]
            if year and year != pub.get("year"):
                changes["year"] = year
        if changes:
            updates.append({"file": f"data/publications/{slug}.yaml", "changes": changes})
    write_out("metadata_updates.json", {"updates": updates, "problems": problems})
    print(f"{len(updates)} publications with metadata updates, {len(problems)} problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())
