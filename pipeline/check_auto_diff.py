"""Gate for automatic merging. Exit 0 only if a change is low-risk.

A pull request labelled `auto` merges without review only if this passes.
Rules: it may only modify (never add, delete, or rename) existing data files,
and in each file only the fields listed below may differ. It may also add
(never remove) entries in data/rejected.yaml.
Anything else must wait for a person.

Usage: python pipeline/check_auto_diff.py BASE_SHA HEAD_SHA   (run inside the repo)
"""
import subprocess
import sys

import yaml

ALLOWED = {
    "data/publications/": {"status", "volume", "issue", "pages", "year"},
}
# The routine may add entries to the rejected list (papers it judged irrelevant),
# so they are reported once and not every week. It may never remove entries.
APPEND_ONLY = "data/rejected.yaml"


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
        if path == APPEND_ONLY and status == "M":
            old = yaml.safe_load(git("show", f"{base}:{path}")) or {}
            new = yaml.safe_load(git("show", f"{head}:{path}")) or {}
            grew = set(new) == {"dois", "urls"} and all(
                set(old.get(k) or []) <= set(new.get(k) or []) for k in ("dois", "urls"))
            if not grew:
                failures.append(f"{path}: entries may only be added, never removed")
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
