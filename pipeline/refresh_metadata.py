"""Propose low-risk metadata completions for publications already on the site.

For each publication with a DOI, ask Crossref for the current record. Only
these fields may change through the auto path: status, volume, issue, pages,
year. Pages are written in APA 7 form (see common.apa_pages). The year is the
print year: it follows Crossref's published-print year whenever there is one,
which moves an online-first paper to its print year once it gets a volume.

Usage: python pipeline/refresh_metadata.py
Output: pipeline/out/metadata_updates.json
"""
import sys
import urllib.parse

from common import apa_pages, fetch_json, load_yaml_dir, write_out


def main():
    updates, problems = [], []
    for slug, pub in load_yaml_dir("publications").items():
        doi = pub.get("doi")
        if not doi:
            continue
        payload = fetch_json("https://api.crossref.org/works/" + urllib.parse.quote(doi))
        if payload is None:
            problems.append(f"Crossref lookup failed for {slug}")
            continue
        record = payload.get("message", {})
        changes = {}
        found = {
            "volume": record.get("volume"),
            "issue": record.get("issue"),
            "pages": apa_pages(record.get("page"), record.get("article-number")),
        }
        for field, value in found.items():
            if value and str(value) != str(pub.get(field) or ""):
                changes[field] = str(value)
        year = ((record.get("published-print") or {}).get("date-parts") or [[None]])[0][0]
        if record.get("volume") and pub.get("status") == "in_press":
            changes["status"] = "published"
            year = year or ((record.get("published") or {}).get("date-parts") or [[None]])[0][0]
        if year and year != pub.get("year"):
            changes["year"] = year
        if changes:
            updates.append({"file": f"data/publications/{slug}.yaml", "changes": changes})
    write_out("metadata_updates.json", {"updates": updates, "problems": problems})
    print(f"{len(updates)} publications with metadata updates, {len(problems)} problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())
