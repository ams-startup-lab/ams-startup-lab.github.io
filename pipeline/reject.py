"""Record rejected candidates so they are never proposed again.

Called by the reject-on-close workflow with the data files a closed
(not merged) candidate pull request would have added.

Usage: python pipeline/reject.py FILE [FILE ...]
"""
import sys
from pathlib import Path

import yaml

from common import DATA, norm_doi, norm_url


def main():
    path = DATA / "rejected.yaml"
    rejected = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    dois, urls = list(rejected.get("dois") or []), list(rejected.get("urls") or [])
    for name in sys.argv[1:]:
        file = Path(name)
        if file.suffix != ".yaml" or not file.exists():
            continue
        try:
            item = yaml.safe_load(file.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        doi, url = norm_doi(item.get("doi")), norm_url(item.get("url"))
        if doi and doi not in dois:
            dois.append(doi)
        elif not doi and url and url not in urls:
            urls.append(url)
    path.write_text(yaml.safe_dump({"dois": sorted(dois), "urls": sorted(urls)}, sort_keys=True), encoding="utf-8")
    print(f"rejected list now holds {len(dois)} DOIs and {len(urls)} URLs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
