#!/usr/bin/env python3
"""Check character limits and reference links for this skill.

Usage: python scripts/check_limits.py [skill_dir]
Exit code 0 when every check passes, 1 otherwise.
"""
import sys
from pathlib import Path

# SKILL.md loads on every trigger, so it gets the tighter budget.
SKILL_MD_LIMIT = 1000
# Reference, script and eval files load one at a time on demand.
OTHER_LIMIT = 2000
# Generated content, not part of the authored skill.
SKIP_DIRS = {"__pycache__", ".git", "results"}


def main() -> int:
    default = Path(__file__).resolve().parent.parent
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else default
    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        print(f"FAIL  no SKILL.md in {root}")
        return 1

    failed = False
    files = sorted(p for p in root.rglob("*") if p.is_file()
                   and not SKIP_DIRS & set(p.relative_to(root).parts))
    for path in files:
        rel = path.relative_to(root).as_posix()
        limit = SKILL_MD_LIMIT if path == skill_md else OTHER_LIMIT
        try:
            # Code points, not bytes, so non-ASCII text counts fairly.
            count = len(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            print(f"FAIL  {rel}: not UTF-8 text")
            failed = True
            continue
        ok = count <= limit
        failed |= not ok
        note = "" if ok else f"  (over by {count - limit})"
        print(f"{'ok  ' if ok else 'FAIL'}  {count:>5}/{limit}  {rel}{note}")

    # Unlinked references are never discovered by the model.
    body = skill_md.read_text(encoding="utf-8")
    for ref in sorted((root / "references").glob("*.md")):
        link = f"references/{ref.name}"
        if link not in body:
            print(f"FAIL  {link} is not linked from SKILL.md")
            failed = True

    print("FAILED" if failed else "All checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
