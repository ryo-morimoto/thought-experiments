#!/usr/bin/env python3
"""te の固定した版を取得し、te 形式の思考実験の記録をすべて検査する。

te は ryo-morimoto/plugins の thought-experiments プラグインに同梱されている
（設計: plugins/thought-experiments/docs/te-design.md）。使う版は根の te.lock に固定する。

  python3 tools/te_check.py                 te.lock の版を取得し、experiments/ 以下の
                                            experiment.toml を持つディレクトリをすべて te check する
  python3 tools/te_check.py --update <sha>  その commit を取得し、te.lock を書き換える

取得した te は .tmp/te/<commit>/ に置く（.gitignore 済み）。commit を全桁で固定し、
git がオブジェクトのハッシュを検証するので、取得した中身はその commit と一致する。
そのうえで te.lock の bundle_sha256（te.py、telib/、data/ をまとめたハッシュ）を照合する。
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCK = ROOT / "te.lock"
CACHE = ROOT / ".tmp" / "te"
REPO = "https://github.com/ryo-morimoto/plugins"
SKILL = "plugins/thought-experiments/skills/running-thought-experiments"


def git(*args: str, cwd: Path) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def fetch(repo: str, commit: str) -> Path:
    """repo の commit を CACHE/<commit> に取得し、te.py のパスを返す。"""
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise SystemExit(f"commit は 40 桁の sha で書く: {commit!r}")
    d = CACHE / commit
    te = d / SKILL / "scripts/te.py"
    if te.exists() and git("rev-parse", "HEAD", cwd=d) == commit:
        return te
    d.mkdir(parents=True, exist_ok=True)
    git("init", "-q", cwd=d)
    git("fetch", "-q", "--depth", "1", repo, commit, cwd=d)
    git("checkout", "-q", "--detach", "FETCH_HEAD", cwd=d)
    if git("rev-parse", "HEAD", cwd=d) != commit:
        raise SystemExit(f"取得した commit が {commit} と一致しない")
    return te


def te_run(te: Path, *args: str) -> int:
    return subprocess.run([sys.executable, "-I", str(te), *args], cwd=ROOT).returncode


def experiments() -> list[Path]:
    return sorted(p.parent for p in (ROOT / "experiments").rglob("experiment.toml"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--update", metavar="COMMIT", help="この commit に te.lock を書き換える")
    a = ap.parse_args()

    if a.update:
        te = fetch(REPO, a.update)
        return te_run(te, "lock", str(LOCK), "--repo", REPO)

    lock = tomllib.loads(LOCK.read_text(encoding="utf-8"))
    te = fetch(lock["repo"], lock["commit"])
    if te_run(te, "version", "--verify", str(LOCK)):
        return 1
    dirs = experiments()
    print(f"te 形式の記録: {len(dirs)} 件")
    failed = [d for d in dirs if (print(f"== {d.relative_to(ROOT)}") or te_run(te, "check", str(d)))]
    for d in failed:
        print(f"FAILED {d.relative_to(ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
