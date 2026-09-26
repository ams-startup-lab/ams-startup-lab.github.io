"""Guard against invented or wrong news items.

A news or media item may be proposed only if this script passes it:
the URL answers with status 200, and the page text names the lab or a member
(full name, or initial and surname as in "Y. Mei", "L De Cuyper" or "Mei, Y.").
The title and date printed here come from the page itself. Use them, not
values from memory.

Usage: python pipeline/verify_url.py URL [URL ...]
Output: JSON on stdout, one object per URL. Exit code 1 if any URL fails.
"""
import html
import json
import re
import sys

from common import fetch, load_rejected, load_yaml_dir, norm_url

LAB_NAMES = ["amsterdam startup lab"]
META = r'<meta[^>]+(?:property|name)=["\']{}["\'][^>]+content=["\']([^"\']+)'
DATE_KEYS = ["article:published_time", "og:published_time", "date", "dc.date", "parsely-pub-date"]


def name_pattern(name):
    """Match a member's full name, or the initial-and-surname forms used in lists."""
    words = name.lower().split()
    full = r"\s+".join(map(re.escape, words))
    if len(words) < 2:
        return re.compile(rf"\b{full}\b")
    initial, surname = re.escape(words[0][0]), r"\s+".join(map(re.escape, words[1:]))
    return re.compile(rf"\b(?:{full}|{initial}(?:\.\s*|\s+){surname})\b|\b{surname},\s*{initial}\b")


def meta(body, key):
    match = re.search(META.format(re.escape(key)), body, re.I)
    return html.unescape(match.group(1)).strip() if match else None


def check(url, members, known, rejected):
    result = {"url": url, "ok": False, "reason": None}
    if norm_url(url) in known:
        result["reason"] = "already on the site"
        return result
    if norm_url(url) in rejected:
        result["reason"] = "previously rejected"
        return result
    status, final_url, body = fetch(url)
    result["status"] = status
    if status != 200:
        result["reason"] = f"HTTP status {status}"
        return result
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", body, flags=re.S | re.I)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text)).lower()
    named = [slug for slug, m in members.items() if name_pattern(m["name"]).search(text)]
    lab = any(name in text for name in LAB_NAMES)
    if not named and not lab:
        result["reason"] = "page names neither the lab nor a member"
        return result
    title = meta(body, "og:title")
    if not title:
        match = re.search(r"<title>([^<]+)", body, re.I)
        title = html.unescape(match.group(1)).strip() if match else None
    date = next((d for d in (meta(body, k) for k in DATE_KEYS) if d), None)
    result.update({
        "ok": True,
        "final_url": final_url,
        "title": title,
        "date": date[:10] if date else None,  # None means: ask the reviewer, do not guess
        "outlet": meta(body, "og:site_name"),
        "members": named,
        "names_lab": lab,
    })
    return result


def main():
    urls = sys.argv[1:]
    if not urls:
        print(__doc__)
        return 2
    members = load_yaml_dir("members")
    known = {norm_url(n.get("url")) for n in load_yaml_dir("news").values()}
    rejected = load_rejected()["urls"]
    results = [check(u, members, known, rejected) for u in urls]
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
