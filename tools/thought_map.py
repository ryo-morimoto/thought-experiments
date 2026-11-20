#!/usr/bin/env python3
"""思考実験の地図。2 つの軸（なるべく標準や論文の分類）で問いの空間を区切り、
どのセルが埋まっていて、次にどこを考えるべきかを出す。依存は標準ライブラリだけ（Python 3.11+）。

地図は maps/<name>/map.toml に書き（雛形: templates/map.toml）、MAP.md はそこから生成する。

使い方:
    python3 tools/thought_map.py frontier maps/<name>     # 次に考える候補を番号付きで出す
    python3 tools/thought_map.py frontier maps/<name> --json
    python3 tools/thought_map.py render [maps/<name> ...]  # MAP.md を再生成（省略時はすべて）
    python3 tools/thought_map.py check                     # 形式の検査と、MAP.md が最新かの検査
"""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAPS = ROOT / "maps"
MAP_FILE, OUT_FILE = "map.toml", "MAP.md"

# 状態 → (記号, 説明)。「埋まった」とみなすのは SETTLED だけ。
STATUS = {
    "unexplored": ("·", "未探索（セルの記述がない）"),
    "open": ("?", "問いだけがある"),
    "hypothesis": ("△", "仮説はあるが裏付けがない"),
    "supported": ("◎", "根拠のある結論"),
    "refuted": ("✕", "仮説が否定された（否定されたこと自体が結論）"),
    "contested": ("!", "根拠が衝突している"),
    "out_of_scope": ("—", "この地図では扱わない（理由を claim に書く）"),
}
SETTLED = {"supported", "refuted"}
MODES = {"constructive", "destructive", "exploratory"}
BASES = {"standard", "paper", "own"}


@dataclass
class Option:
    """次に考える候補。target はセルなら "row/col"、軸なら "axis:rows" など。"""
    score: int
    kind: str
    target: str
    title: str
    why: str
    mode: str


# ---------- 読み込みと検査 ----------

def load(path: Path) -> dict:
    p = path / MAP_FILE if path.is_dir() else path
    m = tomllib.loads(p.read_text(encoding="utf-8"))
    m["_path"] = p
    m["_cells"] = {(c.get("row"), c.get("col")): c for c in m.get("cells", [])}
    return m


def validate(m: dict) -> list[str]:
    where = m["_path"].relative_to(ROOT)
    errs = []
    for k in ("title", "question", "rows", "cols"):
        if k not in m:
            errs.append(f"{where}: {k} がない")
    if errs:
        return errs
    ids = {}
    for ax in ("rows", "cols"):
        a = m[ax]
        for k in ("name", "basis", "ref", "values"):
            if k not in a:
                errs.append(f"{where}: [{ax}] に {k} がない")
        if a.get("basis") not in BASES:
            errs.append(f"{where}: [{ax}].basis は {sorted(BASES)} のどれか")
        vals = [v.get("id") for v in a.get("values", [])]
        if len(vals) != len(set(vals)) or None in vals:
            errs.append(f"{where}: [{ax}] の値の id が欠けているか重複している")
        ids[ax] = set(vals)
    seen = set()
    for c in m.get("cells", []):
        key = (c.get("row"), c.get("col"))
        label = f"{where}: セル {key[0]}/{key[1]}"
        if key in seen:
            errs.append(f"{label} が重複している")
        seen.add(key)
        if key[0] not in ids["rows"] or key[1] not in ids["cols"]:
            errs.append(f"{label} の row/col が軸の値にない")
        st = c.get("status")
        if st not in STATUS or st == "unexplored":
            errs.append(f"{label}: status は {sorted(set(STATUS) - {'unexplored'})} のどれか")
        if st != "open" and not c.get("claim"):
            errs.append(f"{label}: open 以外は claim（結論・仮説・扱わない理由）を書く")
        if c.get("mode") and c["mode"] not in MODES:
            errs.append(f"{label}: mode は {sorted(MODES)} のどれか")
        for e in c.get("evidence", []):
            local = e.split("#")[0]
            if "://" not in e and not (ROOT / local).exists():
                errs.append(f"{label}: 根拠 {e} が見つからない")
    return errs


# ---------- 次に考える候補 ----------

def status(m: dict, r: str, c: str) -> str:
    return m["_cells"].get((r, c), {}).get("status", "unexplored")


def name(m: dict, ax: str, vid: str) -> str:
    return next(v["name"] for v in m[ax]["values"] if v["id"] == vid)


def frontier(m: dict) -> list[Option]:
    rows = [v["id"] for v in m["rows"]["values"]]
    cols = [v["id"] for v in m["cols"]["values"]]
    out = []

    # 軸そのもの: 自作の分類だと、分類が見落としている値に気づけない
    for ax in ("rows", "cols"):
        a = m[ax]
        if a["basis"] == "own":
            out.append(Option(75, "axis", f"axis:{ax}", f"軸「{a['name']}」の根拠を探す",
                              "自作の分類なので、既存の標準・論文の分類と突き合わせると欠けている値が見つかる可能性がある",
                              "exploratory"))
        elif not a.get("checked"):
            out.append(Option(50, "axis", f"axis:{ax}", f"軸「{a['name']}」の出典を確認する",
                              f"出典（{a['ref']}）の本文で値の定義をまだ確かめていない", "exploratory"))

    for r in rows:
        for c in cols:
            cell = m["_cells"].get((r, c), {})
            st = status(m, r, c)
            here = f"{name(m, 'rows', r)} × {name(m, 'cols', c)}"
            target = f"{r}/{c}"
            if st == "contested":
                out.append(Option(100, "cell", target, here,
                                  f"根拠が衝突している（{cell['claim']}）。どの前提が違うのかを特定する", "destructive"))
            elif st == "hypothesis":
                out.append(Option(80, "cell", target, here,
                                  f"仮説「{cell['claim']}」に反例がないか。反例がなければ根拠を足して確定させる", "destructive"))
            elif st == "open":
                q = cell.get("next") or cell.get("claim") or "問いが置かれている"
                out.append(Option(70, "cell", target, here, f"問い「{q}」に答える", "constructive"))
            elif st in SETTLED and not cell.get("evidence"):
                out.append(Option(65, "cell", target, here, "結論に根拠が書かれていない。根拠を足すか、仮説に戻す", "destructive"))
            elif st == "unexplored":
                out.append(_unexplored(m, r, c, rows, cols, here, target))

    out.sort(key=lambda o: -o.score)
    return out


def _unexplored(m, r, c, rows, cols, here, target) -> Option:
    """空のセル。同じ行・列の結論から、どう推論すればよいかを出す。"""
    in_row = [(cc, m["_cells"][(r, cc)]) for cc in cols if status(m, r, cc) in SETTLED]
    in_col = [(rr, m["_cells"][(rr, c)]) for rr in rows if status(m, rr, c) in SETTLED]
    score = 40 + 10 * min(len(in_row), 2) + 10 * min(len(in_col), 2)
    if in_row and in_col:
        (cc, a), (rr, b) = in_row[0], in_col[0]
        why = (f"同じ行の「{name(m, 'cols', cc)}」では「{a['claim']}」、同じ列の「{name(m, 'rows', rr)}」では"
               f"「{b['claim']}」。両方を前提にすると、このセルで何が言えるかを組み立てる")
        mode = "constructive"
    elif in_row or in_col:
        ax, (vid, x) = ("cols", in_row[0]) if in_row else ("rows", in_col[0])
        why = (f"隣の「{name(m, ax, vid)}」の結論「{x['claim']}」がここにも移るか。"
               "移らないなら、何が違うせいかを条件を変えて探す")
        mode = "destructive" if x["status"] == "supported" else "constructive"
    else:
        empty_row = all(status(m, r, cc) == "unexplored" for cc in cols)
        empty_col = all(status(m, rr, c) == "unexplored" for rr in rows)
        where = "行も列もまったく手がついていない" if empty_row and empty_col else "近くに結論がない"
        why = f"{where}。まず問いを立てて、何が起きうるかを広く出す"
        mode = "exploratory"
    return Option(score, "cell", target, here, why, mode)


# ---------- MAP.md ----------

def render(m: dict) -> str:
    rows, cols = m["rows"], m["cols"]
    rel = m["_path"].relative_to(ROOT)
    up = "../" * (len(rel.parts) - 1)
    L = [f"<!-- {rel} から tools/thought_map.py render で生成。直接編集しない -->", "",
         f"# {m['title']}", "", f"**問い**: {m['question']}", ""]

    L += ["## 軸", ""]
    for ax, label in (("rows", "行"), ("cols", "列")):
        a = m[ax]
        basis = {"standard": "標準", "paper": "論文", "own": "自作（既存の分類に置き換える候補）"}[a["basis"]]
        checked = "本文を確認済み" if a.get("checked") else "本文は未確認"
        ref = a["ref"] if "://" in a["ref"] else f"{up}{a['ref']}"
        L.append(f"- **{label}: {a['name']}** — 根拠: {basis}。[{a.get('ref_title', a['ref'])}]({ref})（{checked}）")
        if a.get("note"):
            L.append(f"  - {a['note']}")
        for v in a["values"]:
            L.append(f"  - `{v['id']}` {v['name']}" + (f" — {v['note']}" if v.get("note") else ""))
    L.append("")

    L += ["## 地図", "", "<!-- data-source: original -->"]
    L.append("| | " + " | ".join(v["name"] for v in cols["values"]) + " | 埋まり |")
    L.append("|---|" + "---|" * (len(cols["values"]) + 1))
    for r in rows["values"]:
        cells = [STATUS[status(m, r["id"], c["id"])][0] for c in cols["values"]]
        n = sum(status(m, r["id"], c["id"]) in SETTLED for c in cols["values"])
        L.append(f"| **{r['name']}** | " + " | ".join(cells) + f" | {n}/{len(cells)} |")
    tot = sum(status(m, r["id"], c["id"]) in SETTLED for r in rows["values"] for c in cols["values"])
    col_n = [sum(status(m, r["id"], c["id"]) in SETTLED for r in rows["values"]) for c in cols["values"]]
    L.append("| 埋まり | " + " | ".join(f"{n}/{len(rows['values'])}" for n in col_n)
             + f" | **{tot}/{len(rows['values']) * len(cols['values'])}** |")
    L += ["", "凡例: " + "　".join(f"{s} {d}" for s, d in STATUS.values()), ""]

    L += ["## セル", ""]
    for c in sorted(m.get("cells", []), key=lambda c: (_idx(rows, c["row"]), _idx(cols, c["col"]))):
        sym = STATUS[c["status"]][0]
        L.append(f"### {sym} {name(m, 'rows', c['row'])} × {name(m, 'cols', c['col'])} (`{c['row']}/{c['col']}`)")
        L.append("")
        if c.get("claim"):
            L.append(c["claim"])
            L.append("")
        for e in c.get("evidence", []):
            L.append(f"- 根拠: [{e}]({e if '://' in e else up + e})")
        if c.get("mode"):
            L.append(f"- 最後に回したモード: {c['mode']}")
        if c.get("next"):
            L.append(f"- 次の問い: {c['next']}")
        L.append("")

    L += ["## 次に考える候補", "", "`python3 tools/thought_map.py frontier " + str(rel.parent) + "` と同じ内容。", ""]
    for i, o in enumerate(frontier(m), 1):
        L.append(f"{i}. **{o.title}** (`{o.target}`, {o.mode}) — {o.why}")
    return "\n".join(L) + "\n"


def _idx(axis: dict, vid: str) -> int:
    return [v["id"] for v in axis["values"]].index(vid)


# ---------- CLI ----------

def all_maps() -> list[Path]:
    return sorted(p.parent for p in MAPS.glob(f"*/{MAP_FILE}"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("frontier", help="次に考える候補")
    f.add_argument("map", type=Path)
    f.add_argument("--top", type=int, default=10)
    f.add_argument("--json", action="store_true")
    r = sub.add_parser("render", help="MAP.md を生成")
    r.add_argument("maps", type=Path, nargs="*")
    sub.add_parser("check", help="形式と MAP.md の鮮度を検査")
    a = ap.parse_args()

    if a.cmd == "frontier":
        m = load(a.map.resolve())
        if errs := validate(m):
            print("\n".join(errs), file=sys.stderr)
            return 1
        opts = frontier(m)[: a.top]
        if a.json:
            print(json.dumps([asdict(o) for o in opts], ensure_ascii=False, indent=2))
        else:
            for i, o in enumerate(opts, 1):
                print(f"{i}. [{o.score}] {o.title}  ({o.target}, {o.mode})\n   {o.why}")
        return 0

    paths = [p.resolve() for p in a.maps] if a.cmd == "render" and a.maps else all_maps()
    errs = []
    for p in paths:
        m = load(p)
        if e := validate(m):
            errs += e
            continue
        out = m["_path"].parent / OUT_FILE
        text = render(m)
        if a.cmd == "render":
            out.write_text(text, encoding="utf-8")
            print(f"書き出し: {out.relative_to(ROOT)}")
        elif not out.exists() or out.read_text(encoding="utf-8") != text:
            errs.append(f"{out.relative_to(ROOT)} が {MAP_FILE} と一致しない。"
                        "python3 tools/thought_map.py render を実行する")
    if errs:
        print("\n".join(errs), file=sys.stderr)
        return 1
    if a.cmd == "check":
        print(f"地図 {len(paths)} 件: 問題なし")
    return 0


if __name__ == "__main__":
    sys.exit(main())
