#!/usr/bin/env python3
"""思考実験 experiments/2026-11-21-naming-skill-one-pass.md の具体例を再現する。

ryo-morimoto/plugins の PR #24 で、命名の見直しを4回くり返した後のコミット d64ae13 にも、
一度も使われていない CSS クラス `flag` が残っていた。手作業の見直しでは見落とし、
名前の機械的な数え上げ（naming_inventory.py --unused）では見つかる。

使い方: python3 experiments/scripts/reproduce_naming_unused.py
依存は標準ライブラリだけ。公開リポジトリから1ファイルを取得する（保存はしない）。
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

COMMITS = {"最初（af39591）": "af39591", "4回の見直しの後（d64ae13）": "d64ae13"}
PATHS = {
    "af39591": "plugins/thought-experiments/skills/mapping-thought-experiments/scripts/map_page.py",
    "d64ae13": "plugins/thought-experiments/skills/mapping-thought-experiments/scripts/thought_map.py",
}
INVENTORY = Path(__file__).with_name("naming_inventory.py")


def main() -> int:
    for label, ref in COMMITS.items():
        url = f"https://raw.githubusercontent.com/ryo-morimoto/plugins/{ref}/{PATHS[ref]}"
        with urllib.request.urlopen(url, timeout=30) as r, tempfile.TemporaryDirectory() as d:
            f = Path(d) / Path(PATHS[ref]).name
            f.write_bytes(r.read())
            out = subprocess.run([sys.executable, str(INVENTORY), str(f), "--unused"],
                                 capture_output=True, text=True, check=True).stdout
        hits = [line.split("\t")[:2] for line in out.splitlines() if line.startswith("css-class\tflag")]
        print(f"{label}: 未使用の CSS クラス flag {'あり' if hits else 'なし'}  ({url})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
