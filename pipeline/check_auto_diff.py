"""Gate for automatic merging. Exit 0 only if a change is low-risk.

A pull request labelled `auto` merges without review only if this passes.
Rules: it may only modify (never add, delete, or rename) existing data files,
and in each file only the fields listed below may differ.
Anything else must wait for a person.

Usage: python pipeline/check_auto_diff.py BASE_SHA HEAD_SHA   (run inside the repo)
"""
import subprocess
import sys

import yaml

ALLOWED = {
    "data/publications/": {"status", "volume", "issue", "pages", "year"},
}
ALLOWED_WHOLE_FILES = set()  # no whole-file exceptions at present


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    base, head = sys.argv[1:]
    failures = []
    lines = git("diff", "--name-status", "--no-renames", base, head).splitlines()
    if not lines:
        failures.append("empty diff")
    for line in lines:
        status, path = line.split("\t", 1)
        if path in ALLOWED_WHOLE_FILES and status == "M":
            continue
        fields = next((f for prefix, f in ALLOWED.items() if path.startswith(prefix) and path.endswith(".yaml")), None)
        if fields is None:
            failures.append(f"{path}: not a file the auto path may touch")
            continue
        if status != "M":
            failures.append(f"{path}: auto path may only modify existing files (status {status})")
            continue
        try:
            old = yaml.safe_load(git("show", f"{base}:{path}")) or {}
            new = yaml.safe_load(git("show", f"{head}:{path}")) or {}
        except yaml.YAMLError as err:
            failures.append(f"{path}: invalid YAML ({err})")
            continue
        changed = {k for k in set(old) | set(new) if old.get(k) != new.get(k)}
        extra = changed - fields
        if extra:
            failures.append(f"{path}: fields not allowed on the auto path: {sorted(extra)}")
    for failure in failures:
        print("BLOCKED", failure)
    if not failures:
        print("OK: low-risk change")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
