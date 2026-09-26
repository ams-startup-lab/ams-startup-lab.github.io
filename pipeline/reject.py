"""Record rejected candidates so they are never proposed again.

Called by the reject-on-close workflow with the data files a closed
(not merged) candidate pull request would have added. Items that are already
on the site (for example because a duplicate pull request was merged) are
never recorded as rejected.

Usage: python pipeline/reject.py FILE [FILE ...]
"""
import sys
from pathlib import Path

import yaml

from common import DATA, load_yaml_dir, norm_doi, norm_url


def main():
    path = DATA / "rejected.yaml"
    rejected = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    dois, urls = list(rejected.get("dois") or []), list(rejected.get("urls") or [])
    live = [item for name in ("publications", "news") for item in load_yaml_dir(name).values()]
    live_dois = {norm_doi(item.get("doi")) for item in live} - {None}
    live_urls = {norm_url(item.get("url")) for item in live} - {None}
    for name in sys.argv[1:]:
        file = Path(name)
        if file.suffix != ".yaml" or not file.exists():
            continue
        try:
            item = yaml.safe_load(file.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        doi, url = norm_doi(item.get("doi")), norm_url(item.get("url"))
        if doi in live_dois or url in live_urls:
            print(f"{file.name} is already on the site; not recorded")
            continue
        if doi and doi not in dois:
            dois.append(doi)
        elif not doi and url and url not in urls:
            urls.append(url)
    path.write_text(yaml.safe_dump({"dois": sorted(dois), "urls": sorted(urls)}, sort_keys=True), encoding="utf-8")
    print(f"rejected list now holds {len(dois)} DOIs and {len(urls)} URLs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
