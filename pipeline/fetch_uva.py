"""Check each member's UvA profile page.

UvA profiles do not print a job title. They give the name with its prefix
("Dr.", "Prof. dr.") in <title>, and the page disappears when someone leaves.
This script reports both. It never concludes that a member left: a missing
page only produces a note for the digest.

Usage: python pipeline/fetch_uva.py
Output: pipeline/out/uva_profiles.json
"""
import html
import re
import sys

from common import fetch, load_yaml_dir, write_out


def main():
    members = load_yaml_dir("members")
    report = []
    for slug, member in members.items():
        url = member.get("uva_url")
        if not url or member.get("left"):
            continue
        status, _, body = fetch(url)
        match = re.search(r"<title>([^<]+)", body or "")
        heading = html.unescape(match.group(1)).split(" - ")[0].strip() if match else None
        surname = member["name"].split()[-1].lower()
        entry = {"member": slug, "url": url, "status": status, "heading": heading, "note": None}
        if status != 200 or not heading:
            entry["note"] = "fetch failed or page missing; no change made, check by hand"
        elif surname not in heading.lower():
            entry["note"] = "page does not name this member; no change made, check by hand"
        else:
            prefix = heading.split("(")[0]
            entry["is_professor"] = "prof" in prefix.lower()
        report.append(entry)
    write_out("uva_profiles.json", {"profiles": report})
    flagged = [e for e in report if e["note"]]
    print(f"{len(report)} profiles checked, {len(flagged)} flagged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
